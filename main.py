# Importing Libraries
from nicegui import ui
import requests
from bs4 import BeautifulSoup
from functools import cache
import re
import datetime
import json
from typing import Any
from bot import Bot

# Nation and zones codes dictionary constants
NATIONS: dict = {
    "Austria": "AT",
    "Belgium": "BE",
    "Bulgaria": "BG",
    "Croatia": "HR",
    "Cyprus": "CY",
    "Czechia": "CZ",
    "Denmark": "DK",
    "Estonia": "EE",
    "Finland": "FI",
    "France": "FR",
    "Germany": "DE",
    "Greece": "GR",
    "Hungary": "HU",
    "Iceland": "IS",
    "Ireland": "IE",
    "Italy": "IT",
    "Latvia": "LV",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Malta": "MT",
    "Monaco": "MC",
    "Netherlands": "NL",
    "Norway": "NO",
    "Poland": "PL",
    "Portugal": "PT",
    "Romania": "RO",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Spain": "ES",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Turkey": "TR",
}
ZONES: dict = {
    "Ireland": {
        "Carlow": "CW",
        "Cavan": "CN",
        "Clare": "CE",
        "Cork": "CO",
        "Donegal": "DL",
        "Dublin": "D",
        "Galway": "G",
        "Kerry": "KY",
        "Kildare": "KE",
        "Kilkenny": "KK",
        "Laois": "LS",
        "Leitrim": "LM",
        "Limerik": "LK",
        "Longford": "LD",
        "Louth": "LH",
        "Mayo": "MO",
        "Meath": "MH",
        "Monaghan": "MN",
        "Offaly": "OY",
        "Roscommon": "RN",
        "Sligo": "SO",
        "Tipperary": "TA",
        "Waterford": "WD",
        "Westmeath": "WH",
        "Wexford": "WX",
        "Wicklow": "WW",
    },
    "Italy": {
        "Agrigento": "AG",
        "Alessandria": "AL",
        "Ancona": "AN",
        "Aosta": "AO",
        "Arezzo": "AR",
        "Ascoli Piceno": "AP",
        "Asti": "AT",
        "Avellino": "AV",
        "Bari": "BA",
        "Barletta-Andria-Trani": "BT",
        "Belluno": "BL",
        "Benevento": "BN",
        "Bergamo": "BG",
        "Biella": "BI",
        "Bologna": "BO",
        "Bolzano": "BZ",
        "Brescia": "BS",
        "Brindisi": "BR",
        "Cagliari": "CA",
        "Caltanissetta": "CL",
        "Campobasso": "CB",
        "Carbonia-Iglesias": "CI",
        "Caserta": "CE",
        "Catania": "CT",
        "Catanzaro": "CZ",
        "Chieti": "CH",
        "Como": "CO",
        "Cosenza": "CS",
        "Cremona": "CR",
        "Crotone": "KR",
        "Cuneo": "CN",
        "Enna": "EN",
        "Fermo": "FM",
        "Ferrara": "FE",
        "Firenze": "FI",
        "Foggia": "FG",
        "Forlì-Cesena": "FC",
        "Frosinone": "FR",
        "Genova": "GE",
        "Gorizia": "GO",
        "Grosseto": "GR",
        "Imperia": "IM",
        "Isernia": "IS",
        "La Spezia": "SP",
        "L'Aquila": "AQ",
        "Latina": "LT",
        "Lecce": "LE",
        "Lecco": "LC",
        "Livorno": "LI",
        "Lodi": "LO",
        "Lucca": "LU",
        "Macerata": "MC",
        "Mantova": "MN",
        "Massa-Carrara": "MS",
        "Matera": "MT",
        "Medio Campidano": "VS",
        "Messina": "ME",
        "Milano": "MI",
        "Modena": "MO",
        "Monza E Brianza": "MB",
        "Napoli": "NA",
        "Novara": "NO",
        "Nuoro": "NU",
        "Ogliastra": "OG",
        "Olbia-Tempio": "OT",
        "Oristano": "OR",
        "Padova": "PD",
        "Palermo": "PA",
        "Parma": "PR",
        "Pavia": "PV",
        "Perugia": "PG",
        "Pesaro E Urbino": "PU",
        "Pescara": "PE",
        "Piacenza": "PC",
        "Pisa": "PI",
        "Pistoia": "PT",
        "Pordenone": "PN",
        "Potenza": "PZ",
        "Prato": "PO",
        "Ragusa": "RG",
        "Ravenna": "RA",
        "Reggio Calabria": "RC",
        "Reggio Emilia": "RE",
        "Rieti": "RI",
        "Rimini": "RN",
        "Roma": "RM",
        "Rovigo": "RO",
        "Salerno": "SA",
        "Sassari": "SS",
        "Savona": "SV",
        "Siena": "SI",
        "Siracusa": "SR",
        "Sondrio": "SO",
        "Taranto": "TA",
        "Teramo": "TE",
        "Terni": "TR",
        "Torino": "TO",
        "Trapani": "TP",
        "Trento": "TN",
        "Treviso": "TV",
        "Trieste": "TS",
        "Udine": "UD",
        "Varese": "VA",
        "Venezia": "VE",
        "Verbano-Cusio-Ossola": "VB",
        "Vercelli": "VC",
        "Verona": "VR",
        "Vibo Valentia": "VV",
        "Vicenza": "VI",
        "Viterbo": "VT",
    },
    "Portugal": {
        "Azores": "PT-20",
        "Aveiro": "PT-01",
        "Beja": "PT-02",
        "Braga": "PT-03",
        "Bragança": "PT-04",
        "Castelo Branco": "PT-05",
        "Coimbra": "PT-06",
        "Évora": "PT-07",
        "Faro": "PT-08",
        "Guarda": "PT-09",
        "Leiria": "PT-10",
        "Lisbon": "PT-11",
        "Madeira": "PT-30",
        "Portalegre": "PT-12",
        "Porto": "PT-13",
        "Santarém": "PT-14",
        "Setúbal": "PT-15",
        "Viana do Castelo": "PT-16",
        "Vila Real": "PT-17",
        "Viseu": "PT-18",
    },
    "Romania": {
        "Alba": "AB",
        "Arad": "AR",
        "Argeș": "AG",
        "Bacău": "BC",
        "Bihor": "BH",
        "Bistrița-Năsăud": "BN",
        "Botoșani": "BT",
        "Brăila": "BR",
        "Brașov": "BV",
        "București": "B",
        "Buzău": "BZ",
        "Călărași": "CL",
        "Caraș-Severin": "CS",
        "Cluj": "CJ",
        "Constanța": "CT",
        "Covasna": "CV",
        "Dâmbovița": "DB",
        "Dolj": "DJ",
        "Galați": "GL",
        "Giurgiu": "GR",
        "Gorj": "GJ",
        "Harghita": "HR",
        "Hunedoara": "HD",
        "Ialomița": "IL",
        "Iași": "IS",
        "Ilfov": "IF",
        "Maramureș": "MM",
        "Mehedinți": "MH",
        "Mureș": "MS",
        "Neamț": "NT",
        "Olt": "OT",
        "Prahova": "PH",
        "Sălaj": "SJ",
        "Satu Mare": "SM",
        "Sibiu": "SB",
        "Suceava": "SV",
        "Teleorman": "TR",
        "Timiș": "TM",
        "Tulcea": "TL",
        "Vâlcea": "VL",
    },
    "Spain": {
        "A Coruña": "C",
        "Álava": "VI",
        "Albacete": "AB",
        "Alicante": "A",
        "Almería": "AL",
        "Asturias": "O",
        "Ávila": "AV",
        "Badajoz": "BA",
        "Barcelona": "B",
        "Burgos": "BU",
        "Cáceres": "CC",
        "Cádiz": "CA",
        "Cantabria": "S",
        "Castellón": "CS",
        "Ciudad Real": "CR",
        "Córdoba": "CO",
        "Cuenca": "CU",
        "Gerona": "GI",
        "Granada": "GR",
        "Guadalajara": "GU",
        "Guipúzcoa": "SS",
        "Huelva": "H",
        "Huesca": "HU",
        "Islas Balears": "PM",
        "Jaén": "J",
        "La Coruña": "C",
        "La Rioja": "LO",
        "Las Palmas": "GC",
        "León": "LE",
        "Lérida": "L",
        "Lugo": "LU",
        "Madrid": "M",
        "Málaga": "MA",
        "Murcia": "MU",
        "Navarra": "NA",
        "Orense": "OR",
        "Palencia": "P",
        "Pontevedra": "PO",
        "Salamanca": "SA",
        "Santa Cruz de Tenerife": "TF",
        "Segovia": "SG",
        "Sevilla": "SE",
        "Soria": "SO",
        "Tarragona": "T",
        "Teruel": "TE",
        "Toledo": "TO",
        "Valencia": "V",
        "Valladolid": "VA",
        "Vizcaya": "BI",
        "Zamora": "ZA",
        "Zaragoza": "Z",
    },
}


# Util function to get all the drop dates for the current release
@cache
def get_drop_dates() -> list:
    """
    Fetches drop dates for the current release from Supreme Community website.

    Returns:
        list: A list of drop dates in string format.
        Returns an empty list if the request fails or no dates are found.
    """
    # Drops Site
    url: str = "https://www.supremecommunity.com/season/spring-summer2025/droplists/"

    # Fetching the source code
    response: requests.models.Response = requests.get(url)
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        # Find all dates
        dates_divs: list = soup.find_all("div", {"class": "week-item-subtitle"})
        dates: list[str] = [date.text for date in dates_divs]

        return dates

    else:
        # Return an empty list or handle the error as needed
        return list()


# Util function to convert a date to a certain format
@cache
def convert_date(date: str) -> str:
    """
    Converts a date string into a formatted date string (YYYY-MM-DD).

    Args:
        date (str): The date string to be converted.

    Returns:
        formatted_date (str): The formatted date string.

    Raises:
        ValueError: If the input date string format is incorrect.
    """
    # Remove the ordinal suffix (st, nd, rd) from the date string
    date: str = re.sub(r"(\d)(st|nd|rd|th)( |$)", r"\1\3", date)

    # Parse the date using the modified format
    date_obj: datetime.datetime = datetime.datetime.strptime(date, "%d %B %y")
    formatted_date: str = date_obj.strftime("%Y-%m-%d")

    return formatted_date


# Util function to fetch all information based on drop date and item category
@cache
def fetch_items(drop_date: str, item_category: str) -> dict:
    """
    Fetches information about items based on the specified drop date and item category
    from the Supreme Community website.

    Args:
        drop_date (str): The drop date in string format.
        item_category (str): The category of items to fetch.

    Returns:
        dict: A dictionary containing information about fetched items.
            Keys are item names and values are dictionaries with item details.
    """

    # Converting the tops-sweater option
    if item_category == "Tops":
        item_category: str = "tops-sweaters"

    # Constructing URL based on the Drop Date
    url: str = (
        f"https://www.supremecommunity.com/season/spring-summer2024/droplist/{convert_date(drop_date)}"
    )

    # Creating an Object to store the fetched items
    items_dict: dict = dict()

    # Initializing item_divs to an empty list
    item_divs: list = list()

    # Fetching all items of a certain type
    response: requests.models.Response = requests.get(url)
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        item_divs: list = soup.find_all(
            "div", {"data-category": f"{item_category.lower()}"}
        )

    # Storing Items' Infos
    for item in item_divs:
        item_name: str = item.find(
            "div", {"class": "catalog-item__title"}
        ).text.replace("\n", "")
        item_price: str = (
            item.find("span", {"class": "catalog-label-price"})
            .text.replace("\n", "")
            .split("/")[0]
            if item.find("span", {"class": "catalog-label-price"})
            else "None"
        )
        item_image: str = f'https://www.supremecommunity.com{item.find("img")["src"]}'
        item_colors: list = list()
        item_full_link: str = (
            f'https://www.supremecommunity.com{item.find("a")["href"]}'
        )
        response: requests.models.Response = requests.get(item_full_link)
        if item_price != "None" and response.status_code == 200:
            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
            colors_div: list = soup.find_all(
                "div", {"class": "product-options active"}
            )[1]
            item_colors: list = [
                color.text.replace("\n", "")
                for color in colors_div.find_all("div", {"class": "product-option"})
            ]
            # Removing the VOTE button (not a color option, but a public pool)
            if "VOTING >" in item_colors:
                item_colors.remove("VOTING >")
        item_votes: tuple[str, str] = (
            soup.find("div", {"class": "like"}).text,
            soup.find("div", {"class": "dislike"}).text,
        )
        item_type: str = item["data-category"]
        items_dict[item_name.strip()] = {
            "category": item_type.strip(),
            "price": item_price.strip(),
            "image": item_image,
            "colors": [color.strip() for color in item_colors if type(color) == str],
            "link": item_full_link,
            "votes": item_votes,
        }

    return items_dict


# Function to get the number of items in the basket
def get_number_of_items() -> None:

    # Get the absolute path to the JSON file
    json_file_path: str = "items.json"
    n: int = 0
    try:
        with open(json_file_path, "r") as json_file:
            data: str = json.load(json_file)
            for _ in data:
                n += 1
            return n
    except FileNotFoundError:
        return "JSON file not found"
    except json.JSONDecodeError:
        return "Invalid JSON data"


# Return a customized input component (with app desing guidlines)
def custom_input(placeholder: str | None = None, on_change=None) -> ui.input:
    return (
        ui.input(None, placeholder=placeholder, on_change=on_change)
        .props("square outlined color=black")
        .classes("font-mono")
    )


# Return a customized select component (with app desing guidlines)
def custom_select(
    options: list | dict = [], *, label: Any = None, value: Any = None, on_change=None
) -> ui.select:
    return (
        ui.select(options=options, label=label, value=value, on_change=on_change)
        .props("square outlined color=black")
        .classes("font-mono")
    )


# Creating the Basket object and its UI
class BasketCheckout:
    def __init__(self, notifier: ui.badge, container: ui.grid) -> None:

        # Objects properties
        self.items_number: int = get_number_of_items()
        self.notifier: ui.badge = notifier
        with container:
            self.recap_container: ui.column = ui.column(align_items="stretch").classes(
                "pr-4"
            )
            self.checkout_container: ui.column = ui.column(
                align_items="stretch"
            ).classes("pl-4")
        self.file_path: str = "items.json"
        self.checkout_already_rendered: bool = False
        self.bot: Bot = Bot(NATIONS, ZONES)

        # Rendering the basket
        self.render()

    # Utility to check if the basket is empty
    def is_empty(self) -> bool:
        """
        Checks if the basket JSON file is empty.

        Returns:
            bool: True if the JSON file is empty or doesn't exist, False otherwise.
        """
        try:
            with open(self.file_path, "r") as file:
                data: str = json.load(file)
                if not data:
                    return True  # JSON file is empty
                else:
                    return False  # JSON file is not empty
        except (FileNotFoundError, json.JSONDecodeError):
            return True  # Error occurred or file doesn't exist

    # Function to check if an item is inside the basket
    def item_in(self, item_name: str) -> None:

        try:
            # Load existing items from the JSON file if it exists
            with open(self.file_path, "r") as json_file:
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

    # Function to update the number of item
    def update_number_of_item(self) -> None:

        # Updating the internal number state
        self.items_number: int = get_number_of_items()

        # Updating the badge on the icon
        n: int = get_number_of_items()
        self.notifier.set_text(str(n))
        self.notifier.set_visibility(n >= 1)
        self.notifier.update()

    # Function to render only the recap
    def render_recap(self) -> None:

        # Always cllearing the wrapper before
        self.recap_container.clear()

        # Checking frist if the basket isn't empty
        if not self.is_empty():

            # Loading the basket data from the json file
            with open(self.file_path, "r") as json_file:
                data: str = json.load(json_file)

            # Using the column wrapped in the passed constructor container
            total: int = 0
            with self.recap_container:
                ui.label("Basket").classes("font-mono font-bold text-xl")
                for i, item in enumerate(data):
                    with ui.row(align_items="stretch").classes("pb-4"):
                        with ui.column():
                            ui.label(item["name"]).classes(
                                "font-mono font-bold text-base"
                            )
                            if item["color"] != "None":
                                ui.label(item["color"]).classes("font-mono")
                            if item["size"] != "None":
                                ui.label(item["size"]).classes("font-mono")
                        ui.space()
                        if item["price"] != "None":
                            total += int(item["price"].replace("$", ""))
                            if i == len(data) - 1:
                                with ui.column(align_items="stretch"):
                                    with ui.row():
                                        ui.space()
                                        ui.label(item["price"]).classes(
                                            "font-mono font-bold text-base"
                                        )
                                    ui.space()
                                    ui.label(f"Total: ${total}").classes(
                                        "font-mono font-bold text-base"
                                    )
                            else:
                                ui.label(item["price"]).classes(
                                    "font-mono font-bold text-base"
                                )

    # Function to render only the row for zones options if possible
    def render_zone(self) -> None:

        # Checking if the selected country falls inside the country zones options
        if self.bot.COUNTRY in ["Ireland", "Italy", "Portugal", "Romania", "Spain"]:
            zones: list[str] = [zone for zone in ZONES[self.bot.COUNTRY].keys()]
            with ui.grid(columns="1fr 1fr"):
                custom_input("Postal Code").bind_value_to(self.bot, "POSTAL_CODE")
                custom_select(zones, value=zones[0])
            with ui.grid(columns="1fr 1fr"):
                custom_input("City").bind_value_to(self.bot, "CITY")
                custom_input("Name on Card").bind_value_to(self.bot, "NAME_ON_CARD")
        else:
            with ui.grid(columns="1fr 1fr"):
                custom_input("Postal Code").bind_value_to(self.bot, "POSTAL_CODE")
                custom_input("City").bind_value_to(self.bot, "CITY")
            custom_input("Name on Card").bind_value_to(self.bot, "NAME_ON_CARD")

    # Function to render only the checkout
    def render_checkout(self) -> None:

        # Checking frist if the basket isn't empty
        if not self.is_empty():

            # Setting the first rendering to true
            self.checkout_already_rendered: bool = True

            # Using the column wrapped in the passed constructor container
            with self.checkout_container:
                ui.label("Checkout").classes("font-mono font-bold text-xl")
                custom_input("Email").bind_value_to(self.bot, "EMAIL")
                nations_card_grid: ui.grid = ui.grid(columns="1fr 1fr")
                details_exp_grid: ui.grid = ui.grid(columns="1fr 1fr 1fr 1fr")
                address_cvv_grid: ui.grid = ui.grid(columns="1fr 1fr")
                zones_grid: ui.grid = ui.grid(columns="1fr 1fr")
                phone_checkout_grid: ui.grid = ui.grid(columns="1fr 1fr")
                with nations_card_grid:
                    custom_select(
                        [nation for nation in NATIONS.keys()],
                        value="Austria",
                        on_change=lambda _: self.reload(zones_grid),
                    ).bind_value_to(self.bot, "COUNTRY")
                    custom_input("Card Number").bind_value_to(self.bot, "CARD_NUMBER")
                with details_exp_grid:
                    custom_input("Name").bind_value_to(self.bot, "FIRST_NAME")
                    custom_input("Surname").bind_value_to(self.bot, "LAST_NAME")
                    custom_input("Exp. Year").bind_value_to(self.bot, "YEAR_EXP")
                    custom_input("Exp. Month").bind_value_to(self.bot, "MONTH_EXP")
                with address_cvv_grid:
                    custom_input("Address").bind_value_to(self.bot, "ADDRESS")
                    custom_input("CVV").bind_value_to(self.bot, "CVV")
                with zones_grid:
                    self.render_zone()
                with phone_checkout_grid:
                    custom_input("Phone").bind_value_to(self.bot, "PHONE")
                    ui.button(
                        "Start Supremebot", on_click=lambda _: self.bot.start()
                    ).props(f"square fill color=red-600").classes("font-mono")

    # Util fucntion to reload the checkout based on conutry zone relationships
    def reload(self, container: ui.grid) -> None:

        container.clear()
        with container:
            self.render_zone()

    # Function to render the basket recap
    def render(self) -> None:

        self.render_recap()
        self.render_checkout()


# Creating the Item UI and logic blueprint
class Item(ui.grid):
    def __init__(self, name: str, info: dict, basket: BasketCheckout) -> None:

        # Initializing the basic grid
        super().__init__(columns="2fr 4fr 1fr")
        self.classes("pt-4")

        # Assigning passed parameters to self variables
        self.name: str = name
        self.info: str = info
        self.selected_color = "None"
        self.selected_size = "None"
        self.basket: BasketCheckout = basket

        # Rendering the item
        self.render()

    # Renders the item UI inside the grid
    def render(self) -> None:

        # Using the grid to place the items, in two states: "in" or "not in" basket
        self.clear()
        with self:

            # Render the item image
            with ui.element("div").style(
                "border-width: 1px; border-color: rgb(194, 194, 194);"
            ).classes("p-4 w-fit"):
                ui.image(self.info["image"]).style("width: 11.7rem;")

            # Name, price and trend (if founded)
            with ui.column():
                with ui.row(align_items="center").classes("pt-2"):
                    ui.markdown("**Product**").classes("font-mono text-lg")
                    ui.link(self.name, self.info["link"]).classes(
                        "font-mono font-bold text-black text-lg"
                    )
                    self.trend()
                with ui.row(align_items="center").classes("pt-2"):
                    ui.markdown(f"**Price**").classes("font-mono text-lg")
                    ui.label(self.info["price"]).classes("font-mono text-lg")

                # Render the cta (call to action) "add to basket" or "remove from basket"
                if not self.basket.item_in(self.name):
                    ui.button("add to", on_click=lambda _: self.add_to_basket()).props(
                        f"square fill color=red-600 icon-right=shopping_cart"
                    ).classes("font-mono mt-2")
                else:
                    ui.button(
                        "remove from", on_click=lambda _: self.remove_from_basket()
                    ).props(
                        f"square outline color=red-600 icon-right=shopping_cart"
                    ).classes(
                        "font-mono mt-2"
                    )

            # Render the customize buttons area
            with ui.column(align_items="stretch").classes("pt-2"):

                # Filtering the sizes' options
                size_options: list[str] = (
                    "None"
                    if self.info["category"]
                    not in [
                        "t-shirts",
                        "sweatshirts",
                        "jackets",
                        "tops-sweaters",
                        "pants",
                        "shirts",
                    ]
                    else ["Small", "Medium", "Large", "XLarge", "XXLarge"]
                )
                if not self.basket.item_in(self.name):

                    # Creating the title (if the customize options are availbale)
                    if self.info["colors"] or size_options != "None":
                        ui.label("Customize").classes(
                            "text-lg text-bold font-mono pt-2"
                        )

                    if self.info["colors"]:
                        ui.select(
                            options=self.info["colors"],
                            label="Select a color",
                            value=self.info["colors"][0],
                        ).props("square outlined color=black").classes(
                            "font-mono pt-2"
                        ).bind_value_to(
                            self, "selected_color"
                        )

                    if size_options != "None":
                        ui.select(
                            options=size_options,
                            label="Select a size",
                            value=size_options[0],
                        ).props("square outlined color=black").classes(
                            "font-mono pt-2"
                        ).bind_value_to(
                            self, "selected_size"
                        )

    # Function to add the item to the basket
    def add_to_basket(self) -> None:
        """
        Adds an item to the basket by appending its details to the items.json file
        """
        # Creating the item dict to convert in json format
        item_object: dict = {
            "name": self.name,
            "color": self.selected_color,
            "size": self.selected_size,
            "price": self.info["price"],
            "category": self.info["category"],
        }

        try:
            # Load existing items from the JSON file if it exists
            with open(self.basket.file_path, "r") as json_file:
                basket: list = json.load(json_file)
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty basket
            basket: list = list()

        # Append the new item to the basket
        basket.append(item_object)

        # Write the updated basket to the JSON file
        with open(self.basket.file_path, "w") as json_file:
            json.dump(basket, json_file, indent=4)

        # Updating the basket
        self.basket.update_number_of_item()
        self.basket.render_recap()
        if not self.basket.checkout_already_rendered:
            self.basket.render_checkout()
        if self.basket.is_empty():
            self.basket.checkout_container.clear()
            self.basket.checkout_already_rendered = False

        # Refreshing the item UI
        self.render()

    # Function to remove the item from the baskt
    def remove_from_basket(self) -> None:
        """
        Removes an item with the specified name from the basket stored in items.json file
        """
        try:
            # Load existing items from the JSON file if it exists
            with open(self.basket.file_path, "r") as json_file:
                basket: list = json.load(json_file)
        except FileNotFoundError:
            # If the file doesn't exist, there are no items to delete
            return False

        # Create a flag to check if the item was found and deleted
        item_deleted: bool = False

        # Create a copy of the basket to avoid modifying it during iteration
        basket_copy: list = basket.copy()

        # Iterate through items in the basket
        for item in basket_copy:
            if item.get("name") == self.name:
                basket.remove(item)  # Remove the item from the basket
                item_deleted: bool = True
                break

        if item_deleted:
            # Write the updated basket to the JSON file
            with open(self.basket.file_path, "w") as json_file:
                json.dump(basket, json_file, indent=4)

        # Updating the basket
        self.basket.update_number_of_item()
        self.basket.render_recap()
        if not self.basket.checkout_already_rendered:
            self.basket.render_checkout()
        if self.basket.is_empty():
            self.basket.checkout_container.clear()
            self.basket.checkout_already_rendered = False

        # Refreshing the item UI
        self.render()

    # Function to generate the trend UI for the item
    def trend(self) -> None:

        # Calculate the ratio, ensure 'dislikes' is non-zero by adding 1
        try:
            ratio: float = int(self.info["votes"][0]) / (
                int(self.info["votes"][1]) + 1
            )  # Prevents division by zero

            # Display trending status based on the ratio
            if ratio >= 3:
                with ui.icon("local_fire_department").classes("text-2xl text-red-600"):
                    ui.tooltip("Trending").classes("bg-red-600 font-mono").props(
                        "delay=700"
                    )
        except:
            with ui.icon("info").classes("text-2xl text-grey"):
                ui.tooltip("No info yet").classes("bg-grey font-mono").props(
                    "delay=700"
                )


# Creating the Items List UI and logic blueprint
class ItemsList:
    def __init__(self, basket: BasketCheckout, container: ui.column) -> None:

        # Creating a date and category parameter to use to show items
        self.date: str = get_drop_dates()[0]
        self.category: str = "T-Shirts"
        self.basket: BasketCheckout = basket
        self.container: ui.column = container

    # Render all the Items object inside the column, with the specified date and category
    def render(self) -> None:

        # Fetching the items
        items: dict = fetch_items(self.date, self.category)

        # For each item in the fetched list, render its corresponding component
        self.container.clear()
        for item_name, item_info in items.items():
            with self.container:
                Item(item_name, item_info, self.basket)


# Main app logic
with ui.element("div").classes("w-full p-8"):

    # Creating the main heading
    header: ui.row = ui.row(align_items="center")
    with header:
        with ui.element("div").classes("w-fit bg-red-600"):
            ui.label("Supremebot").classes(
                "text-white text-4xl text-bold italic font-mono"
            )

        # Adding spacing between title and call to action
        ui.space()

        with ui.link(target="https://www.buymeacoffee.com/saccofrancesco"):
            ui.image(
                "https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png"
            ).classes("w-[150px]")

    # Creating the grid for the date and category selectors
    selectors_container: ui.grid = ui.grid(columns="1fr 5fr").classes("py-8")

    # The container for the items list
    list_container: ui.column = ui.column(align_items="stretch")

    # The container for the basket recap UI
    with ui.link_target("basket"):
        footer_container: ui.grid = ui.grid(columns="1.5fr 2fr").classes("pt-10 w-full")

    # Creating the basket with its notifier
    with header:
        items_number: int = get_number_of_items()
        basket_link: ui.link = ui.link(target="#basket").classes("text-black")
        with basket_link:
            basket_icon: ui.icon = ui.icon("shopping_cart", size="2.5rem")
        with basket_icon:
            basket_notifier: ui.badge = (
                ui.badge(items_number, color="red-600")
                .props("floating")
                .classes("font-mono")
            )
        basket_notifier.set_visibility(items_number >= 1)
        basket_notifier.update()

    # Creating the basket object to store basket state
    basket: BasketCheckout = BasketCheckout(basket_notifier, footer_container)

    # Creating the items list section
    items_list: ItemsList = ItemsList(basket, list_container)

    # Creating the select and tabs widgets
    with selectors_container:
        date: ui.select = (
            ui.select(
                options=get_drop_dates(),
                label="Select a drop date",
                value=get_drop_dates()[0],
                on_change=lambda: items_list.render(),
            )
            .props("square outlined color=black")
            .classes("font-mono")
            .bind_value_to(items_list, "date")
        )
        with ui.tabs(
            value="T-Shirts",
            on_change=lambda _: items_list.render(),
        ).props(
            "indicator-color=red-600 align=justify"
        ).classes("font-mono").bind_value_to(items_list, "category") as tabs:
            ui.tab("T-Shirts")
            ui.tab("Accessories")
            ui.tab("Sweatshirts")
            ui.tab("Hats")
            ui.tab("Jackets")
            ui.tab("Tops")
            ui.tab("Pants")
            ui.tab("Skate")
            ui.tab("Bags")
            ui.tab("Shirts")

    # Rendering the list
    items_list.render()

# Running the app
ui.run(title="Supremebot", favicon="img/icon.png")
