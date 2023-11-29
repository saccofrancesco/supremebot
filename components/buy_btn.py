# Importing Libraries
import streamlit as st
from bot.bot import Bot
from playwright.sync_api import sync_playwright, TimeoutError
import time


class BuyButtonUI:
    def __init__(self) -> None:

        self.buy_btn = st.button("BUY", key="buy-btn", type="primary")
        if self.buy_btn:
            print("start...")
            # Creating the Bot
            bot: Bot = Bot()

            start_time = time.time()
            # Start the automation
            bot.scrape()
            end_time = time.time()
            print(f"Time For Scrayping Items: {end_time - start_time} s.")

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                bot.add_to_basket(page)

                try:
                    bot.checkout(page)
                    end_time = time.time()
                    print(f"Time For Checkout: {end_time - start_time} s.")
                except TimeoutError:
                    # Handle timeout
                    print("Timeout while performing checkout")
                end_time = time.time()
                print(f"Total Time: {end_time - start_time} s.")

                input()  # input() を使用することで、プログラムがすぐに終了するのを防ぎ、ユーザーが結果を確認する時間を確保
