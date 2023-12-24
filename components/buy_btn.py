# Importing Libraries
import streamlit as st
from bot.bot import Bot
from playwright.sync_api import sync_playwright, TimeoutError

class BuyButtonUI:
    def __init__(self) -> None:
        # Create a button in the Streamlit UI
        self.buy_btn: bool = st.button(
            "Start Supremebot",
            key="buy-btn",
            type="primary",
            use_container_width=True
        )

        # If the button is clicked, start the Supremebot
        if self.buy_btn:
            self.run_supremebot()

    def run_supremebot(self) -> None:
        try:
            # Creating an instance of the Supremebot
            bot: Bot = Bot()

            # Start the automation process
            bot.scrape()

            # Set up Playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                # Add items to the basket
                bot.add_to_basket(page)

                try:
                    # Attempt to complete the checkout process
                    bot.checkout(page)
                except TimeoutError:
                    st.warning("Checkout process timed out.")
        except Exception as e:
            # Handle any exceptions that occur during the Supremebot execution
            st.error(f"An error occurred: {e}")
