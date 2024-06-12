# Importing libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import re
import json
from components.zones import *
from components.checkout import CheckoutUI
import os

# Function to initialize the program
@st.cache_data
def init() -> None:
    """
    Initializes the program by injecting CSS for image styling and creating necessary directories and files.
    """
    # Injecting CSS for image styling
    st.markdown(
        "<style> img { border-radius: 5%; } </style>",
        unsafe_allow_html=True)
    
    # Create the directory if it doesn't exist
    if not os.path.exists("./config"):
        os.makedirs("./config")

    # Write data (empty list) to the JSON file (if the file doesn't exists)
    if not os.path.exists("./config/items.json"):
        with open("./config/items.json", 'w') as json_file:
            json.dump([], json_file, indent=4)

# Util function to get all the drop dates for the current release
@st.cache_data
def get_drop_dates() -> list:
    """
    Fetches drop dates for the current release from Supreme Community website.

    Returns:
        list: A list of drop dates in string format.
            Returns an empty list if the request fails or no dates are found.
    """
    # Drops Site
    url: str = "https://www.supremecommunity.com/season/spring-summer2024/droplists/"

    # Fetching the source code
    response: requests.models.Response = requests.get(url)
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        # Find all dates
        dates_divs: list = soup.find_all("div", {"class": "week-item-subtitle"})
        dates: list = [date.text for date in dates_divs]

        return dates

    else:
        # Return an empty list or handle the error as needed
        return []

# Util function to convert a date to a certain format
@st.cache_data
def convert_date(date: str) -> str:
    """
    Converts a date string into a formatted date string (YYYY-MM-DD).

    Args:
        date (str): The date string to be converted.

    Returns:
        str: The formatted date string.

    Raises:
        ValueError: If the input date string format is incorrect.
    """
    # Remove the ordinal suffix (st, nd, rd) from the date string
    date: str = re.sub(r'(\d)(st|nd|rd|th)( |$)', r'\1\3', date)

    # Parse the date using the modified format
    date_obj: datetime.datetime = datetime.datetime.strptime(date, "%d %B %y")
    formatted_date: str = date_obj.strftime("%Y-%m-%d")

    return formatted_date

# Util function to fetch all information based on Drop Date and Item Category
def fetch_items(drop_date: str, item_category: str) -> dict:
    """
    Fetches information about items based on the specified drop date and item category from Supreme Community website.

    Args:
        drop_date (str): The drop date in string format.
        item_category (str): The category of items to fetch.

    Returns:
        dict: A dictionary containing information about fetched items.
            Keys are item names and values are dictionaries with item details.
    """
    # Coverting data to url format
    data: str = convert_date(drop_date)

    # Converting the tops-sweater option
    if item_category == "Tops":
        item_category = "tops-sweaters"

    # Constructing URL based on the Drop Date
    url: str = f"https://www.supremecommunity.com/season/spring-summer2024/droplist/{data}"

    # Creating an Object to store the fetched items
    items_dict: dict = {}

    # Initializing item_divs to an empty list
    item_divs: list = []

    # Fetching all items of a certain type
    response: requests.models.Response = requests.get(url)
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        item_divs: list = soup.find_all("div", {"data-category": f"{item_category.lower()}"})

    # Storing Items' Infos
    for item in item_divs:
        item_name: str = item.find(
            "div", {"class": "catalog-item__title"}).text.replace("\n", "")
        item_price: str = item.find("span",
                                    {"class": "catalog-label-price"}).text.replace("\n",
                                                                                   "").split("/")[0] if item.find("span",
                                                                                                                  {"class": "catalog-label-price"}) else "None"
        item_image: str = f'https://www.supremecommunity.com{item.find("img")["src"]}'
        item_colors: list = []
        item_full_link: str = f'https://www.supremecommunity.com{item.find("a")["href"]}'
        response: requests.models.Response = requests.get(item_full_link)
        if item_price != "None" and response.status_code == 200:
            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
            colors_div: list = soup.find_all(
                "div", {"class": "product-options active"})[1]
            item_colors: list = [
                color.text.replace(
                    "\n", "") for color in colors_div.find_all(
                    "div", {
                        "class": "product-option"})]
            # Removing the VOTE button (not a color option, but a public pool)
            if "VOTING >" in item_colors:
                item_colors.remove("VOTING >")
        item_type: str = item["data-category"]
        items_dict[item_name] = {
            "category": item_type,
            "price": item_price,
            "image": item_image,
            "colors": item_colors,
            "link": item_full_link
        }

    return items_dict

# Util function to check if an item is already
def is_item_in_basket(item_name: str) -> bool:
    """
    Checks if an item with the specified name is already in the basket JSON file.

    Args:
        item_name (str): The name of the item to check.

    Returns:
        bool: True if the item is found in the basket, False otherwise.
    """
    # Get the absolute path to the JSON file
    json_file_path = os.path.join("config", "items.json")

    try:
        # Load existing items from the JSON file if it exists
        with open(json_file_path, "r") as json_file:
            basket: list = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, the item is not in the basket
        return False

    # Check if the item_name exists in any of the items
    for item in basket:
        if item.get("name") == item_name:
            return True

    # If the item_name is not found in any item, return False
    return False

# Util function to add an item to the basket (items.json)
def add_to_basket(
        item_image: str,
        item_price: int,
        item_name: str,
        item_color: str,
        item_size: str,
        item_category: str):
    """
    Adds an item to the basket by appending its details to the items.json file.

    Args:
        item_image (str): The URL of the item's image.
        item_price (int): The price of the item.
        item_name (str): The name of the item.
        item_color (str): The color of the item.
        item_size (str): The size of the item.
        item_category (str): The category of the item.
    """
    # Creating the item object
    item_object: dict = {
        "image": item_image,
        "price": item_price,
        "name": item_name,
        "color": item_color,
        "size": item_size,
        "category": item_category
    }

    # Get the absolute path to the JSON file
    json_file_path = os.path.join("config", "items.json")

    try:
        # Load existing items from the JSON file if it exists
        with open(json_file_path, "r") as json_file:
            basket: list = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty basket
        basket: list = []

    # Append the new item to the basket
    basket.append(item_object)

    # Write the updated basket to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(basket, json_file, indent=4)

    # Showing a success message
    st.toast("Item added to the basket", icon="✅")

# Util function to delete an item
def remove_from_basket(item_name: str) -> bool:
    """
    Removes an item with the specified name from the basket stored in items.json file.

    Args:
        item_name (str): The name of the item to remove.

    Returns:
        bool: True if the item was successfully removed, False otherwise.
    """
    # Get the absolute path to the JSON file
    json_file_path = os.path.join("config", "items.json")

    try:
        # Load existing items from the JSON file if it exists
        with open(json_file_path, "r") as json_file:
            basket: list = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, there are no items to delete
        return False

    # Create a flag to check if the item was found and deleted
    item_deleted: bool = False

    # Create a copy of the basket to avoid modifying it during iteration
    basket_copy = basket.copy()

    # Iterate through items in the basket
    for item in basket_copy:
        if item.get("name") == item_name:
            basket.remove(item)  # Remove the item from the basket
            item_deleted = True
            break

    if item_deleted:
        # Write the updated basket to the JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(basket, json_file, indent=4)

        # Showing a success message
        st.toast("Item removed from the basket", icon="❌")

    return item_deleted

# Util function to check if the basket is empty
def is_json_file_empty(file_path: str) -> bool:
    """
    Checks if the specified JSON file is empty.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        bool: True if the JSON file is empty or doesn't exist, False otherwise.
    """
    try:
        with open(file_path, 'r') as file:
            data: str = json.load(file)
            if not data:
                return True  # JSON file is empty
            else:
                return False  # JSON file is not empty
    except (FileNotFoundError, json.JSONDecodeError):
        return True  # Error occurred or file doesn't exist

# Util function to get infos about an item in the basket
def get_info_for_item(item_name: str, param: str):
    """
    Retrieves information about a specific item from the items.json file.

    Args:
        item_name (str): The name of the item to retrieve information for.
        param (str): The parameter or field to retrieve from the item's data.

    Returns:
        str: The value of the specified parameter for the item.
            Returns an error message if the item or parameter is not found.
    """
    # Get the absolute path to the JSON file
    json_file_path = os.path.join("config", "items.json")

    try:
        with open(json_file_path, 'r') as json_file:
            data: str = json.load(json_file)
            for item in data:
                if "name" in item:
                    if item["name"] == item_name:
                        return item.get(param, f"No such parameter: {param}")
            return "Item not found in JSON data"
    except FileNotFoundError:
        return "JSON file not found"
    except json.JSONDecodeError:
        return "Invalid JSON data"

# Util function to list all the available country
@st.cache_data
def country_list() -> list:
    """
    Retrieves a list of all available countries from the NATIONS dictionary.

    Returns:
        list: A list of country names.
    """
    return [nation for nation in NATIONS.keys()]

# Util function to get a selected country and retur the list of his zones
@st.cache_data
def country_zones(country_name: str) -> list:
    """
    Retrieves a list of zones or regions for a specific country from the ZONES dictionary.

    Args:
        country_name (str): The name of the country.

    Returns:
        list: A list of zone names for the specified country.
    """
    return [zone for zone in ZONES[country_name].keys()]

# Util function to save payments data
def save_pay_data(form: CheckoutUI) -> dict:
    """
    Creates a dictionary containing payment information from the CheckoutUI form instance.

    Args:
        form (CheckoutUI): An instance of CheckoutUI containing payment details.

    Returns:
        dict: A dictionary containing payment information.
    """
    # Creating a pay data dict
    return {
        "email": form.email,
        "country": form.country,
        "first_name": form.name,
        "last_name": form.surname,
        "address": form.address,
        "postal_code": form.postal_code,
        "city": form.city,
        "phone": form.phone,
        "card_number": form.card_number,
        "expiration_month": form.expiration_month,
        "expiration_year": form.expiration_year,
        "cvv": form.cvv,
        "name_on_card": form.name_on_card,
        "zone": form.zone if hasattr(form, "zone") else "None"
    }

# Util function to get the next 5 years from current year
@st.cache_data
def get_card_exp_years() -> list:
    """
    Retrieves a list of the next 5 years from the current year for selecting credit card expiration year.

    Returns:
        list: A list of years in string format.
    """
    current_year: datetime.datetime = datetime.datetime.now().year
    next_5_years: list = [str(current_year + i) for i in range(6)]
    return next_5_years

# Util function to get month in a list based on current day
@st.cache_data
def months_in_numbers(selected_year: str):
    """
    Retrieves a list of months in numerical format based on the selected year.

    Args:
        selected_year (str): The selected year in string format.

    Returns:
        list: A list of months in numerical format.
    """
    current_year: datetime.datetime = datetime.datetime.now().year
    current_month: datetime.datetime = datetime.datetime.now().month

    if selected_year == current_year:
        # If the selected year is the current year, return months from the current
        # month to December
        months: list = [str(month) for month in range(current_month, 13)]
    else:
        # For any other year, return all months
        months: list = [str(month) for month in range(1, 13)]

    return months

# Util function to get pay props from pay.config file
def get_pay_prop(prop: str) -> str:
    """
    Retrieves a specific property (e.g., email, country) from the pay.json configuration file.

    Args:
        prop (str): The property to retrieve from the configuration file.

    Returns:
        str: The value of the specified property.
            Returns None if the property is not found or there is an error.
    """
    file_path = os.path.join("config", "pay.json")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data[prop]
    except FileNotFoundError:
        return None  # File not found
    except json.JSONDecodeError:
        return None  # Invalid JSON format in the file
