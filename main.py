# Importing Libraries
import streamlit as st
from components.drop_dates import DropDatesUI
from components.categories import CategoriesUI
from components.item import ItemUI
from components.basket import BasketUI
from components.checkout import CheckoutUI
from components.buy_btn import BuyButtonUI
from components.download_btn import DownloadButtonUI

# Running the App
if __name__ == "__main__":

    # Configuration
    st.set_page_config("Supremebot", "img/icon.png", "wide")

    # Injecting CSS for image styling
    st.markdown(
        "<style> img { border-radius: 5%; } </style>",
        unsafe_allow_html=True)

    # Setting up the dates selection
    dates: DropDatesUI = DropDatesUI()

    # Setting up categories selection
    category: CategoriesUI = CategoriesUI()

    # For each item, show the product card
    ItemUI(category.items_category, dates.selected_date)

    # Showing the basket content if not empty
    basket: BasketUI = BasketUI()

    # Creating a cjeckout form for submitting payments data
    if not basket.is_empty:

        # Form to compile for buying
        form: CheckoutUI = CheckoutUI()

        # Button for saving paying methods
        with form.save_pay_method_col:
            DownloadButtonUI(form)

        # User input to start the Bot
        with form.buy_col:
            buy_btn: BuyButtonUI = BuyButtonUI()
