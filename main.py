# Importing Libraries
from rich.console import Console
from rich.progress import track
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
from sys import exit
import requests
import json

# Creating the Bot Class


class Bot:

    # Constructor
    def __init__(self) -> None:

        # Creating a Console Instance
        self.CONSOLE = Console()

        # Opening the Items File
        with open("Items.json", "r") as i:

            # Loading the JSON File
            ITEMS = json.load(i)

            # Creating the Lists
            self.ITEMS_NAMES = []
            self.ITEMS_STYLES = []
            self.ITEMS_SIZES = []
            self.ITEMS_TYPES = []

            # Looping the JSON File
            for item in ITEMS:

                # Appending the Prameters to the Lists
                self.ITEMS_NAMES.append(item["Item"])
                self.ITEMS_STYLES.append(item["Style"])
                self.ITEMS_SIZES.append(item["Size"])
                self.ITEMS_TYPES.append(item["Type"])

        # Opening the Data File
        with open("Data.json", "r") as d:

            # Loading the JSON File
            DATA = json.load(d)

            # Looping the JSON File
            for info in DATA:

                # Storing Personal Data
                self.NAME_SURNAME = info["Name Surname"]
                self.EMAIL = info["Email"]
                self.TEL = info["Tel"]
                self.ADDRESS = info["Address"]
                self.CITY = info["City"]
                self.COUNTRY = info["Country"]
                self.POSTAL_CODE = info["Postal Code"]
                self.CARD_NUMBER = info["Card Number"]
                self.MONTH_EXP = info["Expiration Month"]
                self.YEAR_EXP = info["Expiration Year"]
                self.CVV = info["CVV"]

        # Creating the Link's List
        self.links_list = []

        # Buy Times
        self.HOUR = "12"
        self.MINUTE = "0"

    # Scrape Method for Saving the URLs
    def scrape(self) -> None:

        # Looping the Items' Types
        for i in track(range(len(self.ITEMS_NAMES)),
                       description="🔗 [blue]Extracting Items' Links...[/blue]"):

            # URL to Scrape
            url = "https://www.supremenewyork.com/shop/all/" + \
                self.ITEMS_TYPES[i]

            # Requesting the URL
            source = requests.get(url).text
            soup = BeautifulSoup(source, "html.parser")

            # Storing all the Links of the Page
            links = [
                "https://www.supremenewyork.com" + link["href"]
                for link in soup.find_all("a", class_="name-link")
            ]

            # Removing the Duplicates
            links = list(dict.fromkeys(links))

            # Checking for the Right Links
            for link in links:

                # Requesting the Link's page
                source = requests.get(link).text
                soup = BeautifulSoup(source, "html.parser")

                # Finding the name and Style of the Item
                name = soup.find("h1", class_="protect").text
                style = soup.find("p", class_="style protect").text

                # Checking if the Item is To Buy
                if name == self.ITEMS_NAMES[i] and style == self.ITEMS_STYLES[i]:

                    # Appending the Link to the List of To Buy
                    self.links_list.append(link)
                    break

    # Method for Add to the Cart the founded Items
    def add_to_basket(self, page) -> None:

        # Looping the Element's to Buy List
        for i in track(range(len(self.links_list)),
                       description="💸 [green]Buying the Items...[/green]"):
            page.goto(self.links_list[i])

            # Requesting the Item's Page
            source = requests.get(self.links_list[i]).text
            soup = BeautifulSoup(source, "html.parser")

            # Checking if Elements have Multiple Sizes
            if soup.find(
                    "select",
                    id="size") and soup.find(
                    "input",
                    type="submit"):

                # Selecting the Right Size
                page.click("#size")
                option = page.query_selector("#size")
                option.select_option(label=self.ITEMS_SIZES[i])

                # Adding the Item to the Cart
                page.click("input.button")

    # Method for Compiling the Checkout Form
    def checkout(self, page) -> None:

        # Performing Actions during an Animation
        with self.CONSOLE.status("🖋️ [yellow]Performing the Checkout...[/yellow]"):

            # Going to the Checkout
            page.click("a.button:nth-child(3)")

            # Using Data to Compile the Form
            # Name, Surname, Email and Tel
            page.fill("#order_billing_name", self.NAME_SURNAME)
            page.fill("#order_email", self.EMAIL)
            page.fill("#order_tel", self.TEL)

            # Address, City, Country and Postal Code
            page.fill("#order_billing_address", self.ADDRESS)
            page.fill("#order_billing_city", self.CITY)
            page.fill("#order_billing_zip", str(self.POSTAL_CODE))
            page.click("#order_billing_country")
            option = page.query_selector("#order_billing_country")
            option.select_option(label=self.COUNTRY.upper())

            # Card Number, Expiration Date and CVV
            page.fill("#credit_card_number", str(self.CARD_NUMBER))
            page.click("#credit_card_month")
            option = page.query_selector("#credit_card_month")
            option.select_option(label=str(self.MONTH_EXP))
            page.click("#credit_card_year")
            option = page.query_selector("#credit_card_year")
            option.select_option(label=str(self.YEAR_EXP))
            page.fill("#credit_card_verification_value", str(self.CVV))


# Main Program
if __name__ == "__main__":

    # Creating the Bot Instance
    BOT = Bot()

    # Create a Loop for Fastest Buying
    while True:

        # Saving the Current Time
        now = datetime.now()

        # Checking if the Current Time == the Time of the Drop (Buy Times)
        if str(now.hour) == BOT.HOUR and str(now.minute) == BOT.MINUTE:

            # Finding the Links for the Requested Elements
            BOT.scrape()

            # Using Playwright API to perform Automatic Actions
            with sync_playwright() as p:

                # Creating a Browser Instance
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                # Adding the Requested Elements to the Cart
                BOT.add_to_basket(page)

                # Performing the Checkout
                BOT.checkout(page)

                # Exit the Script
                exit()
