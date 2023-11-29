# Importing libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import re
import json
from components.zones import *
from components.checkout import CheckoutUI
from io import StringIO

# Util function to get all the drop dates for the current release
@st.cache_data
def get_drop_dates() -> list:

    # Drops Site
    url: str = "https://www.supremecommunity.com/season/fall-winter2023/droplists/"

    # Fetching the source code
    response: requests.models.Response = requests.get(url)
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    # Find all dates
    dates_divs: list = soup.find_all("div", {"class": "week-item-subtitle"})
    dates: list = [date.text for date in dates_divs]

    return dates

# Util function to convert a date to a certain format
@st.cache_data
def convert_date(date: str) -> str:

    # Remove the ordinal suffix (st, nd, rd) from the date string
    date: str = re.sub(r'(\d)(st|nd|rd|th)( |$)', r'\1\3', date)

    # Parse the date using the modified format
    date_obj: datetime.datetime = datetime.datetime.strptime(date, "%d %B %y")
    formatted_date: str = date_obj.strftime("%Y-%m-%d")

    return formatted_date

# Util function to fetch all information based on Drop Date and Item Category
def fetch_items(drop_date: str, item_category: str) -> dict:

    # Coverting data to url format
    data: str = convert_date(drop_date)

    # Constructing URL based on the Drop Date
    url: str = f"https://www.supremecommunity.com/season/fall-winter2023/droplist/{data}/#"

    # Creating an Object to store the fetched items
    items_dict: dict = {}

    # Object for mapping categories to urllike category
    categories: dict = {
        "T-Shirts": "t-shirts",
        "Accessories": "accessories",
        "Sweatshirts": "sweatshirts",
        "Hats": "hats",
        "Jackets": "jackets",
        "Tops-Sweaters": "tops-sweaters",
        "Pants": "pants",
        "Skate": "skate",
        "Bags": "bags",
        "Shirts": "shirts"
    }

    # Fetching all items of a certain type
    response: requests.models.Response = requests.get(url)
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    item_divs: list = soup.find_all(
        "div", {"data-category": f"{categories[item_category]}"})

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
        item_type: str = item["data-category"]
        items_dict[item_name] = {
            "category": item_type,
            "price": item_price,
            "image": item_image,
            "colors": item_colors,
        }

    return items_dict

# Util function to check if an item is already
def is_item_in_basket(item_name: str) -> bool:
    try:

        # Load existing items from the JSON file if it exists
        with open("./config/items.json", "r") as json_file:
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

    # Creating the item object
    item_object: dict = {
        "image": item_image,
        "price": item_price,
        "name": item_name,
        "color": item_color,
        "size": item_size,
        "category": item_category
    }

    try:

        # Load existing items from the JSON file if it exists
        with open("./config/items.json", "r") as json_file:
            basket: list = json.load(json_file)
    except FileNotFoundError:

        # If the file doesn't exist, start with an empty basket
        basket: list = []

    # Append the new item to the basket
    basket.append(item_object)

    # Write the updated basket to the JSON file
    with open("./config/items.json", "w") as json_file:
        json.dump(basket, json_file, indent=4)

    # Showing a succes message
    st.toast("Item added to basket", icon="✅")

# Util function to delete an item
def remove_from_basket(item_name: str) -> bool:
    try:

        # Load existing items from the JSON file if it exists
        with open("./config/items.json", "r") as json_file:
            basket: list = json.load(json_file)
    except FileNotFoundError:

        # If the file doesn't exist, there are no items to delete
        return False

    # Create a flag to check if the item was found and deleted
    item_deleted: bool = False

    # Iterate through items in the basket
    for item in basket:
        if item.get("name") == item_name:
            basket.remove(item)  # Remove the item from the basket
            item_deleted: bool = True
            break

    if item_deleted:

        # Write the updated basket to the JSON file
        with open("./config/items.json", "w") as json_file:
            json.dump(basket, json_file, indent=4)

    # Showing a succes message
    st.toast("Item removed from basket", icon="❌")

# Util function to check if the basket is empty
def is_json_file_empty(file_path: str) -> bool:
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
    try:
        with open("./config/items.json", 'r') as json_file:
            data: str = json.load(json_file)
            for item in data:
                if "name" in item:
                    if item["name"] == item_name:
                        return item[f"{param}"]
            return "Item not found in JSON data"
    except FileNotFoundError:
        return "JSON file not found"
    except json.JSONDecodeError:
        return "Invalid JSON data"

# Util function to list all the available country
@st.cache_data
def country_list() -> list:

    return [nation for nation in NATIONS.keys()]

# Util function to get a selected country and retur the list of his zones
@st.cache_data
def country_zones(country_name: str) -> list:

    return [zone for zone in ZONES[country_name].keys()]

# Util function to save payments data
def save_pay_data(form: CheckoutUI) -> dict:

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
            "card_number" : form.card_number,
            "expiration_month": form.expiration_month,
            "expiration_year": form.expiration_year,
            "cvv": form.cvv,
            "name_on_card": form.name_on_card,
            "zone": form.zone if hasattr(form, "zone") else "None"
        }

# Util function to get the next 5 years from current year
@st.cache_data
def get_card_exp_years() -> list:
    current_year: datetime.datetime = datetime.datetime.now().year
    next_5_years: list = [str(current_year + i) for i in range(6)]
    return next_5_years

# Util function to get month in a list based on current day
def months_in_numbers(selected_year: str):
    current_year: datetime.datetime = datetime.datetime.now().year
    current_month: datetime.datetime = datetime.datetime.now().month

    if selected_year == current_year:
        # If the selected year is the current year, return months from the next month to December
        months: list = [str(month) for month in range(current_month + 1, 13)]
    else:
        # For any other year, return all months
        months: list = [str(month) for month in range(1, 13)]

    return months

# Util function to get pay props from pay.config file
def get_pay_prop(file, prop: str) -> str:

    # Coverting the uploaded file to a readable format
    stringio: StringIO = StringIO(file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data: str = stringio.read()

    try:
        data: str = json.loads(string_data)
        return data[0][prop]
    except FileNotFoundError:
        return None  # File not found
    except json.JSONDecodeError:
        return None  # Invalid JSON format in the file
