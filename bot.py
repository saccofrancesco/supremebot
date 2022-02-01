# Importing Libraries
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

# Supreme Shop Link
SUPREME_SHOP_LINK = 'https://www.supremenewyork.com/shop/all'
SUPREME_PARTIAL_LINK = 'https://www.supremenewyork.com'

# Global Switches xPaths
NEW_XPATH = '/html/body/div[2]/nav/ul/li[2]/a'
JACKETS_XPATH = '/html/body/div[2]/nav/ul/li[3]/a'
SHIRTS_XPATH = '/html/body/div[2]/nav/ul/li[4]/a'
TOPS_SWEATERS_XPATH = '/html/body/div[2]/nav/ul/li[5]/a'
SWEATSHIRTS_XPATH = '/html/body/div[2]/nav/ul/li[6]/a'
PANTS_XPATH = '/html/body/div[2]/nav/ul/li[7]/a'
HATS_XPATH = '/html/body/div[2]/nav/ul/li[8]/a'
BAGS_XPATH = '/html/body/div[2]/nav/ul/li[9]/a'
ACCESSORIES_XPATH = '/html/body/div[2]/nav/ul/li[10]/a'
SHOES_XPATH = '/html/body/div[2]/nav/ul/li[11]/a'
SKATES_XPATH = '/html/body/div[2]/nav/ul/li[12]/a'

# Global UI Elements xPaths
UK_XPATH = '/html/body/footer/nav/ul[2]/li[1]'
IT_XPATH = '/html/body/ul/li[4]'
ADD_TO_BASKET_XPATH = '/html/body/div[2]/div/div[2]/div/form/fieldset[2]/input'
SIZE_XPATH = '/html/body/div[2]/div/div[2]/div/form/fieldset[1]/select'
BUY_NOW_XPATH = '/html/body/div[2]/div/div[1]/div/a[2]'

# Global Payment xPaths
NAME_SURNAME_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[1]/fieldset/div[1]/input'
EMAIL_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[1]/fieldset/div[2]/input'
TEL_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[1]/fieldset/div[3]/input'
ADDRESS_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[1]/fieldset/div[4]/div[1]/input'
CITY_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[1]/fieldset/div[6]/input'
POST_CODE_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[1]/fieldset/div[7]/div[1]/input'
COUNTRY_SELECTOR_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[1]/fieldset/div[7]/div[2]/select'
ITALY_SELECTOR_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[1]/fieldset/div[7]/div[2]/select/option[20]'
CARD_NUMBER_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/div[4]/div[1]/input'
CARD_MONTH_SELECTOR_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/div[4]/div[2]/div[1]/select[1]'
CARD_MONTH_INPUT = '/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/div[4]/div[2]/div[1]/select[1]/option[11]'
CARD_YEAR_SELECTOR_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/div[4]/div[2]/div[1]/select[2]'
YEAR_NUMBER_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/div[4]/div[2]/div[1]/select[2]/option[6]'
CVV_XPATH = '/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/div[4]/div[2]/div[2]/input'

# Define the Bot Class
class Bot:
    # Define the Constructor
    def __init__(self):
        self.driver = webdriver.Chrome('chromedriver.exe')
        # Item's Data
        self.item_name = []
        self.item_style = []
        self.item_size = []
        self.item_type = []
        # Payment's Data
        self.name_surname = ""
        self.email = ""
        self.tel = 0
        self.address = ""
        self.N = ""
        self.city = ""
        self.postal_code = 0
        self.card_number = 0
        self.cvv = 0
        # Scraping Item's Data
        with open("Items.json", "r") as f:
            Item_Dict = json.load(f)
        for Item in Item_Dict:
            self.item_name.append(Item["Item"])
            self.item_style.append(Item["Style"])
            self.item_size.append(Item["Size"])
            self.item_type.append(Item["Type"])
        f.close()
        # Scraping Payment's Data
        with open("Data.json", "r") as d:
            Data_Dict = json.load(d)
        for Data in Data_Dict:
            self.name_surname = Data["Name Surname"]
            self.email = Data["Email"]
            self.tel = Data["Tel"]
            self.address = Data["Address"]
            self.N = Data["N"]
            self.city = Data["City"]
            self.postal_code = Data["Postal Code"]
            self.card_number = Data["Card Number"]
            self.cvv = Data["CVV"]
        d.close()
        # Item's Links Listing
        self.f_links_list = []
        self.items_to_buy_links = []
        # Buy Times
        self.HOUR = "12"
        self.MINUTE = "00"

    # Open Supreme Site and Set Up
    def open_supreme_shop(self):
        self.driver.get(SUPREME_SHOP_LINK)
        btn = self.driver.find_element_by_xpath(UK_XPATH)
        btn.click()
        time.sleep(0.01)
        btn = self.driver.find_element_by_xpath(IT_XPATH)
        btn.click()