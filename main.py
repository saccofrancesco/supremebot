# Importing Libraries
from rich.console import Console
from rich.progress import track
from playwright.sync_api import sync_playwright, TimeoutError
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
                self.ITEMS_TYPES.append(item["Type"].replace("/", "-")) # Preventing tops/sweaters to make error in the link

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
        self.HOUR = "23"
        self.MINUTE = "10"

    # Scrape Method for Saving the URLs
    def scrape(self) -> None:
        for i in track(range(len(self.ITEMS_NAMES)),
                       description="🔗 [blue]Extracting Items' Links...[/blue]"):
            url = f"https://us.supreme.com/collections/{self.ITEMS_TYPES[i]}"

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                page.goto(url)  # Navigate to the URL

                # Wait for dynamic content to load (adjust the wait time as needed)
                page.wait_for_selector("a[data-cy-title]")

                # Extract the links using Playwright
                links = page.query_selector_all("a[data-cy-title]")
                links_list = [link.get_attribute("href") for link in links]

                # Checking for the Right Links
                for link in links_list:
                    complete_link = f"https://us.supreme.com{link}"
                    page.goto(complete_link)  # Navigate to the link

                    # Wait for the product info to load (adjust the wait time as needed)
                    page.wait_for_selector("#product-root > div > div.Product.width-100.js-product.routing-transition.fade-on-routing > div.product-column-right > form > div.width-100 > div > h1")

                    if product_name := page.query_selector(
                        "#product-root > div > div.Product.width-100.js-product.routing-transition.fade-on-routing > div.product-column-right > form > div.width-100 > div > h1"
                    ).inner_text():
                        
                        product_style = page.query_selector("#product-root > div > div.Product.width-100.js-product.routing-transition.fade-on-routing > div.product-column-right > form > div.width-100 > div > div.display-flex.flexWrap-wrap.bpS-bg-none.bg-white.mobile-shadow.pt-m.pb-m.bpS-p-0.flexDirection-columnReverse.bpS-flexDirection-column > div.fontWeight-bold.mb-s.display-none.bpS-display-block.js-variant").inner_text()
                        if len(product_style) >= 2 and product_name == self.ITEMS_NAMES[i] and product_style == self.ITEMS_STYLES[i]:
                            self.links_list.append(complete_link)
                            break

                browser.close()


    # Method for Add to the Cart the founded Items
    def add_to_basket(self, page) -> None:

        # Looping the Element's to Buy List
        for i in track(range(len(self.links_list)),
                       description="💸 [green]Buying the Items...[/green]"):
            page.goto(self.links_list[i])
            print("Adding to basket:", self.links_list[i])  # Debugging print

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
            try:
                page.click('[data-cy="mini-cart-checkout-button"]', timeout=60000)  # Increased timeout
            except TimeoutError:
                print("Timeout while clicking on checkout button")

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
    BOT = Bot()

    while True:
        now = datetime.now()

        if str(now.hour) == BOT.HOUR and str(now.minute) == BOT.MINUTE:
            print("Time to buy!")

            BOT.scrape()

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                BOT.add_to_basket(page)

                try:
                    BOT.checkout(page)
                except TimeoutError:
                    print("Timeout while performing checkout")  # Handle timeout
                finally:
                    browser.close()

                exit()
