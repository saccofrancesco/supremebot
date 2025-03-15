# Importing Libraries
import playwright.async_api
from playwright.async_api import async_playwright, TimeoutError
import requests
import bs4
from bs4 import BeautifulSoup
import json
from nicegui import ui


# Creating the Bot Class
class Bot:
    """
    A class representing a bot for automating the Supreme shopping experience.
    """

    # Constructor
    def __init__(self, nations_codes: dict, zones_codes: dict) -> None:
        """
        Initializes the Bot instance by loading configuration data and setting up required attributes.
        """
        # Opening the Items File
        with open("items.json", "r") as i:

            # Loading the JSON file and looping through
            ITEMS = json.load(i)
            self.ITEMS_NAMES: list[str] = [item["name"] for item in ITEMS]
            self.ITEMS_STYLES: list[str] = [item["color"] for item in ITEMS]
            self.ITEMS_SIZES: list[str] = [item["size"] for item in ITEMS]
            self.ITEMS_TYPES: list[str] = [
                item["category"].replace("/", "-") for item in ITEMS
            ]

        # Storing Personal Data
        self.EMAIL = self.COUNTRY = self.FIRST_NAME = self.LAST_NAME = self.ADDRESS = ""
        self.POSTAL_CODE = self.CITY = self.PHONE = self.CARD_NUMBER = ""
        self.MONTH_EXP = self.YEAR_EXP = self.CVV = self.NAME_ON_CARD = self.ZONE = ""

        # Creating the Link's List
        self.links_list: list[str] = list()

        # Saving the list of nations and zones codes to convert
        self.nations_codes: dict = nations_codes
        self.zones_codes: dict = zones_codes

    def update(self) -> None:
        """
        Updates the bot's personal data based on the user's input.
        """
        # Opening the Items File
        with open("items.json", "r") as i:

            # Loading the JSON file and looping through
            ITEMS = json.load(i)
            self.ITEMS_NAMES: list[str] = [item["name"] for item in ITEMS]
            self.ITEMS_STYLES: list[str] = [item["color"] for item in ITEMS]
            self.ITEMS_SIZES: list[str] = [item["size"] for item in ITEMS]
            self.ITEMS_TYPES: list[str] = [
                item["category"].replace("/", "-") for item in ITEMS
            ]

    # Scrape Method for Saving the URLs
    async def scrape(self) -> None:
        """
        Scrapes the Supreme website to find valid product links based on configured item criteria.
        """
        # Clear the list of links
        self.links_list.clear()

        # Config for the scraping process
        BASE_URL: str = "https://eu.supreme.com/collections/new"
        HEADERS: str = {"User-Agent": "Mozilla/5.0"}

        def fetch_data(url: str) -> dict:
            """Fetch the webpage content and extract the JSON product data."""
            response: requests.models.Response = requests.get(
                url, headers=HEADERS, timeout=10
            )
            response.raise_for_status()  # Ensure request was successful

            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
            script_tag: bs4.element.Tag = soup.find("script", id="products-json")

            if not script_tag or not script_tag.text.strip():
                raise ValueError("No product JSON found on the page.")

            return json.loads(script_tag.text.strip())

        def structure_data(products: list[dict]) -> dict:
            """Organize products by category with only necessary fields."""
            structured: dict = dict()
            for product in products:
                category: str = product.get("product_type", "uncategorized").replace(
                    "/", "-"
                )
                structured.setdefault(category, []).append(
                    {
                        "title": product.get("title"),
                        "color": product.get("color"),
                        "url": product.get("url"),
                        "available": product.get("available"),
                    }
                )
            return {"categories": structured}

        try:
            raw_data: list[dict] = fetch_data(BASE_URL)
            structured_data: dict = structure_data(raw_data.get("products", []))

            # Iterate over the categories provided (from the input lists)
            for i, category in enumerate(self.ITEMS_TYPES):
                products: list[dict] = structured_data["categories"].get(category, [])
                for product in products:
                    if (
                        product.get("available")
                        and product.get("title") == self.ITEMS_NAMES[i]
                        and product.get("color") == self.ITEMS_STYLES[i]
                    ):
                        self.links_list.append(
                            f"https://eu.supreme.com{product.get('url')}"
                        )

        except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
            print(f"Error occurred: {e}")

    # Method for Add to Basket
    async def add_to_basket(self, page: playwright.async_api._generated.Page) -> None:
        """
        Adds items from the collected links to the shopping basket on the Supreme website.
        """
        for i in range(len(self.links_list)):
            await page.goto(self.links_list[i])

            if self.ITEMS_TYPES[i] == "bags":
                await page.click("input[data-type='product-add']")
                continue

            await page.wait_for_selector('select[aria-label="size"]')
            options: playwright.async_api._generated.ElementHandle = page.locator(
                'select[aria-label="size"]'
            )
            if options:
                await options.select_option(self.ITEMS_SIZES[i])
            await page.click('button[data-testid="add-to-cart-button"]')
            await page.wait_for_timeout(1000)

    # Method for Checkout
    async def checkout(self, page: playwright.async_api._generated.Page) -> None:
        """
        Completes the checkout process on the Supreme website.
        """

        # Going to the supreme checkout form link
        await page.goto("https://eu.supreme.com/it/checkout")

        # Accept the terms
        await page.click('input[type="checkbox"]')

        # Filling the Checkout Form
        await page.fill('input[id="email"]', self.EMAIL)
        await page.locator('select[name="countryCode"]').select_option(
            self.nations_codes[self.COUNTRY]
        )
        await page.fill('input[name="firstName"]', self.FIRST_NAME)
        await page.fill('input[name="lastName"]', self.LAST_NAME)
        await page.fill('input[name="address1"]', self.ADDRESS)
        await page.fill('input[name="postalCode"]', self.POSTAL_CODE)
        await page.fill('input[name="city"]', self.CITY)

        try:
            await page.wait_for_selector('select[name="zone"]')
            zone_select = page.locator('select[name="zone"]')
            await zone_select.select_option(self.zones_codes[self.COUNTRY][self.ZONE])
            await page.wait_for_timeout(1500)
        except Exception:
            pass

        await page.fill('input[name="phone"]', self.PHONE)

        # Fill credit card details in iframe
        await page.frame_locator(
            'iframe[src*="checkout.shopifycs.com/number"]'
        ).locator('input[name="number"]').fill(self.CARD_NUMBER)

        await page.frame_locator(
            'iframe[src*="checkout.shopifycs.com/expiry"]'
        ).locator('input[name="expiry"]').fill(f"{self.MONTH_EXP}/{self.YEAR_EXP}")

        await page.frame_locator(
            'iframe[src*="checkout.shopifycs.com/verification_value"]'
        ).locator('input[name="verification_value"]').fill(self.CVV)

        await page.frame_locator('iframe[src*="checkout.shopifycs.com/name"]').locator(
            'input[name="name"]'
        ).fill(self.NAME_ON_CARD)

    # Function to start the bot
    async def start(self) -> None:
        try:

            # Update the info if something is changed
            self.update()

            # Start the automation process
            await self.scrape()

            # Set up Playwright
            async with async_playwright() as p:
                browser: playwright.async_api._generated.Browser = (
                    await p.chromium.launch(headless=False)
                )
                page: playwright.async_api._generated.Page = await browser.new_page()

                # Add items to the basket
                await self.add_to_basket(page)

                try:
                    # Attempt to complete the checkout process
                    await self.checkout(page)

                    # Waiting for the user to submit the order
                    await page.pause()

                except TimeoutError as e:
                    ui.notify(f"Error: {e}")
                    print(e)
        except Exception as e:
            pass
