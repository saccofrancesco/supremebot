# Importing Libraries
import streamlit as st
from bot.bot import Bot
from playwright.sync_api import sync_playwright, TimeoutError

class BuyButtonUI:
    """
    A class to represent the Buy Button User Interface in a Streamlit application.

    Attributes:
        buy_btn (bool): Indicates whether the "Start Supremebot" button was clicked.
    """
    def __init__(self) -> None:
        """
        Initializes the BuyButtonUI instance by creating a button in the Streamlit UI.
        If the button is clicked, starts the Supremebot.
        """
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
        """
        Runs the Supremebot to automate the process of adding items to the basket and checking out.
        Handles exceptions that occur during the execution.
        """
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
