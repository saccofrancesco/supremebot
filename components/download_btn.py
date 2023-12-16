# Importing Libraries
import streamlit as st
from components.utils import save_pay_data
from components.checkout import CheckoutUI
import json
import os

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
            with open(json_file_path, "w") as f:
                f.write(f"[{json.dumps(save_pay_data(form), indent=4)}]")
            st.toast("Payment configuration saved", icon="✅")
