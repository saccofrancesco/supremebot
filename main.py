# Importing Libraries
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from sys import exit

# Bot Class
class Bot:

    # Constructor
    def __init__(self) -> None:

        # Saving Items
        with open("Items.json", "r") as i:
            items_dict = json.load(i)
            self.items_name = []
            self.items_style = []
            self.items_size = []
            self.items_type = []
            for item in items_dict:
                self.items_name.append(item["Item"])
                self.items_style.append(item["Style"])
                self.items_size.append(item["Size"])
                self.items_type.append(item["Type"])

        # Saving Data
        with open("Data.json", "r") as d:
            datas_dict = json.load(d)
            for data in datas_dict:
                self.name_surname = data["Name Surname"]
                self.email = data["Email"]
                self.tel = data["Tel"]
                self.address = data["Address"]
                self.city = data["City"]
                self.country = data["Country"]
                self.postal_code = data["Postal Code"]
                self.card_number = data["Card Number"]
                self.month_exp = data["Expiration Month"]
                self.year_exp = data["Expiration Year"]
                self.cvv = data["CVV"]

        # Item's Links Listing
        self.links_list= []

        # Buy Times
        self.HOUR = "12"
        self.MINUTE = "00"

    # Scrape Method for Saving the urls
    def scrape(self) -> None:

        # Looping the Items' Types
        for i in range(len(self.items_name)):

            # List for Links
            links = []

            # Scraping
            url = "https://www.supremenewyork.com/shop/all/" + self.items_type[i]
            source = requests.get(url).text
            soup = BeautifulSoup(source, "html.parser")
            for link in soup.find_all("a", class_ = "name-link"):
                links.append("https://www.supremenewyork.com" + link["href"])
        
            # Removing Duplicates
            links = list(dict.fromkeys(links))

            # Checking for the Right Link
            for j in range(len(links)):
                source = requests.get(links[j]).text
                soup = BeautifulSoup(source, "html.parser")
                name = soup.find("h1", class_ = "protect").text
                style = soup.find("p", class_ = "style protect").text
                if name == self.items_name[i] and style == self.items_style[i]:
                    self.links_list.append(links[j])
                    break

    # Method for add to the cart the requeted elements
    def addTobasket(self, page) -> None:
        
        # Looping the Element's to Buy List
        for i in range(len(self.links_list)):
            page.goto(self.links_list[i])
            
            # Saving Page Data
            source = requests.get(self.links_list[i]).text
            soup = BeautifulSoup(source, "html.parser")

            # Checking if Elements is Buyable
            if soup.find("select", id = "size") and soup.find("input", type = "submit"):
                page.click("#size")
                option = page.query_selector("#size")
                option.select_option(label = self.items_size[i])
                page.click("input.button")

    # Method for Compiling the Checkout Form
    def checkout(self, page) -> None:

        # Going to the Checkout
        page.click("a.button:nth-child(3)")

        # Using Data to Compile the Form
        page.fill("#order_billing_name", self.name_surname)
        page.fill("#order_email", self.email)
        page.fill("#order_tel", self.tel)
        page.fill("#order_billing_address", self.address)
        page.fill("#order_billing_city", self.city)
        page.fill("#order_billing_zip", str(self.postal_code))
        page.click("#order_billing_country")
        option = page.query_selector("#order_billing_country")
        option.select_option(label = self.country.upper())
        page.fill("#credit_card_number", str(self.card_number))
        page.click("#credit_card_month")
        option = page.query_selector("#credit_card_month")
        option.select_option(label = str(self.month_exp))
        page.click("#credit_card_year")
        option = page.query_selector("#credit_card_year")
        option.select_option(label = str(self.year_exp))
        page.fill("#credit_card_verification_value", str(self.cvv))

# Main Program
if __name__ == "__main__":

    # Creating a Bot Instance
    bot = Bot()

    # Create a Loop for Instants Buying
    while True:
        
        # Saving the Current Time
        now = datetime.now()

        # Checking if the Curretn Time == the Time of the Drop
        if str(now.hour) == bot.HOUR and str(now.minute) == bot.MINUTE:

            # Finding the Links for the Requeted Elemnts
            bot.scrape()

            # Using Playwright API to perform Automatic Actions
            with sync_playwright() as p:

                # Creating a Browser Instance
                browser = p.chromium.launch(headless = False)
                page = browser.new_page()

                # Adding the Requeted Elements to the Basket
                bot.addTobasket(page)

                # Checkout
                bot.checkout(page)

                # Exit the Script
                exit()
