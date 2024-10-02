# Importing Libraries
import streamlit as st
from components.utils import save_pay_data
from components.checkout import CheckoutUI
import json
import os
from typing import Dict


class DownloadButtonUI:
    """
    A class to represent the Download Button User Interface in a Streamlit application.

    Attributes:
        download_btn (bool): Indicates whether the "Save info for next time" button was clicked.
    """

    def __init__(self, form: CheckoutUI) -> None:
        """
        Initializes the DownloadButtonUI instance by creating a button to save payment information.

        Args:
            form (CheckoutUI): An instance of CheckoutUI containing payment information.
        """
        # Get the absolute path to the JSON file
        json_file_path: str = os.path.join("config", "pay.json")

        self.download_btn = st.button(
            "Save info for next time",
            key="save-btn",
            type="secondary",
            use_container_width=True,
        )
        if self.download_btn:
            try:
                self.save_payment_data(json_file_path, form)
                st.toast("Payment configuration saved", icon="✅")
            except Exception as e:
                st.error(f"Error saving payment configuration: {e}")

    @staticmethod
    def save_payment_data(file_path: str, form: CheckoutUI) -> None:
        """
        Static method to save payment data to a JSON file.

        Args:
            file_path (str): Path to the JSON file where payment data will be saved.
            form (CheckoutUI): An instance of CheckoutUI containing payment information.
        """
        # Serialize payment data to JSON and save to file
        payment_data: Dict[str, str] = save_pay_data(form)
        with open(file_path, "w") as f:
            json.dump(payment_data, f, indent=4)
