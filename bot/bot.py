# Importing Libraries
from rich.console import Console
from playwright.sync_api import sync_playwright, TimeoutError
import json
import playwright

# Creating the Bot Class
class Bot:

    # Constructor
    def __init__(self) -> None:

        # Creating a Console Instance
        self.CONSOLE: Console = Console()

        # Opening the Items File
        with open("./config/items.json", "r") as i:

            # Loading the JSON File
            ITEMS: str = json.load(i)

            # Creating the Lists
            self.ITEMS_NAMES: list = []
            self.ITEMS_STYLES: list = []
            self.ITEMS_SIZES: list = []
            self.ITEMS_TYPES: list = []

            # Looping the JSON File
            for item in ITEMS:

                # Appending the Prameters to the Lists
                self.ITEMS_NAMES.append(item["name"])
                self.ITEMS_STYLES.append(item["color"])
                self.ITEMS_SIZES.append(item["size"])
                self.ITEMS_TYPES.append(item["category"].replace("/", "-")) # Preventing tops/sweaters to make error in the link

        # Opening the Data File
        with open("./config/pay.config.json", "r") as d:

            # Loading the JSON File
            DATA: str = json.load(d)

            # Looping the JSON File
            for info in DATA:

                # Storing Personal Data
                self.EMAIL: str = info["email"]
                self.COUNTRY: str = info["country"]
                self.FIRST_NAME: str = info["first_name"]
                self.LAST_NAME: str = info["last_name"]
                self.ADDRESS: str = info["address"]
                self.POSTAL_CODE: str = info["postal_code"]
                self.CITY: str = info["city"]
                self.PHONE: str = info["phone"]
                self.CARD_NUMBER: str = info["card_number"]
                self.MONTH_EXP: str = info["expiration_month"]
                self.YEAR_EXP: str = info["expiration_year"]
                self.CVV : str= info["cvv"]
                self.NAME_ON_CARD: str = info["name_on_card"]
                try:
                    self.ZONE: str = info["zone"]
                except Exception:
                    pass

        # Creating the Link's List
        self.links_list: list = []

    # Scrape Method for Saving the URLs
    def scrape(self) -> None:
        for i in range(len(self.ITEMS_NAMES)):
            url: str = f"https://us.supreme.com/collections/{self.ITEMS_TYPES[i]}"

            with sync_playwright() as p:
                browser: playwright.sync_api._generated.Browser = p.chromium.launch(headless=True)
                page: playwright.sync_api._generated.Browser = browser.new_page()
                page.goto(url)  # Navigate to the URL

                # Wait for dynamic content to load (adjust the wait time as needed)
                page.wait_for_selector("a[data-cy-title]")

                # Extract the links using Playwright
                links: list = page.query_selector_all("a[data-cy-title]")
                links_list: list = [link.get_attribute("href") for link in links]

                # Checking for the Right Links
                for link in links_list:
                    complete_link: str = f"https://us.supreme.com{link}"
                    page.goto(complete_link)  # Navigate to the link

                    # Wait for the product info to load (adjust the wait time as needed)
                    page.wait_for_selector("#product-root > div > div.Product.width-100.js-product.routing-transition.fade-on-routing > div.product-column-right > form > div.width-100 > div > h1")

                    if product_name := page.query_selector(
                        "#product-root > div > div.Product.width-100.js-product.routing-transition.fade-on-routing > div.product-column-right > form > div.width-100 > div > h1"
                    ).inner_text():
                        
                        product_style: str = page.query_selector("#product-root > div > div.Product.width-100.js-product.routing-transition.fade-on-routing > div.product-column-right > form > div.width-100 > div > div.display-flex.flexWrap-wrap.bpS-bg-none.bg-white.mobile-shadow.pt-m.pb-m.bpS-p-0.flexDirection-columnReverse.bpS-flexDirection-column > div.fontWeight-bold.mb-s.display-none.bpS-display-block.js-variant").inner_text()
                        if len(product_style) >= 2 and product_name == self.ITEMS_NAMES[i] and product_style == self.ITEMS_STYLES[i]:
                            self.links_list.append(complete_link)
                            break

                browser.close()

    # Method for Add to the Cart the founded Items
    def add_to_basket(self, page) -> None:

        # Looping the Element's to Buy List
        for i in range(len(self.links_list)):
            page.goto(self.links_list[i])

            page.wait_for_selector("select[data-cy='size-selector']")
            options = page.locator("select[data-cy='size-selector']")
            options.select_option(label=f"{self.ITEMS_SIZES[i]}")
            page.click("input[data-type='product-add']")

    # Method for Compiling the Checkout Form
    def checkout(self, page) -> None:

        # Going to the Checkout
        try:
            page.click('#product-root > div > div.collection-nav.display-none.bpS-display-block > div > div > div > a.button.button--s.c-white.width-100.display-flex.bg-red--aa', timeout=60000)  # Increased timeout
        except TimeoutError:
            pass

        # Using Data to Compile the Form
        page.fill("input[id='email']", self.EMAIL)
        options = page.locator("select[name='countryCode']")
        options.select_option(label=f"{self.COUNTRY}")
        page.fill("input[name='firstName']", self.FIRST_NAME)
        page.fill("input[name='lastName']", self.LAST_NAME)
        page.fill("input[name='address1']", self.ADDRESS)
        page.fill("input[name='postalCode']", self.POSTAL_CODE)
        page.fill("input[name='city']", self.CITY)
        try:
            page.wait_for_selector("select[name='zone']")
            options = page.locator("select[name='zone']")
            options.select_options(label=f"{self.ZONE}")
        except Exception:
            pass
        page.fill("input[name='phone']", self.PHONE)
        page.fill("input[name='number']", self. CARD_NUMBER)
        page.fill("input[name='expiry']", f"{self.MONTH_EXP} / {self.YEAR_EXP}")
        page.fill("input[name='verification_value']", self.CVV)
        page.fill("input[name='name']", self.NAME_ON_CARD)
