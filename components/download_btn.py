# Importing Libraries
import streamlit as st
from components.utils import save_pay_data
from components.checkout import CheckoutUI
import json
import os
from typing import Dict

class DownloadButtonUI:
    def __init__(self, form: CheckoutUI) -> None:
        # Get the absolute path to the JSON file
        json_file_path: str = os.path.join("config", "pay.json")

        self.download_btn = st.button(
            "Save info for next time",
            key="save-btn",
            type="secondary",
            use_container_width=True)
        if self.download_btn:
            try:
                self.save_payment_data(json_file_path, form)
                st.toast("Payment configuration saved", icon="✅")
            except Exception as e:
                st.toast(f"Error saving payment configuration: {e}", icon="❌")

    @staticmethod
    def save_payment_data(file_path: str, form: CheckoutUI) -> None:
        # Serialize payment data to JSON and save to file
        payment_data: Dict[str, str] = save_pay_data(form)
        with open(file_path, "w") as f:
            json.dump(payment_data, f, indent=4)
