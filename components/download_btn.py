# Importing Libraries
import streamlit as st
from components.utils import save_pay_data, sanitize_filename
from components.checkout import CheckoutUI
import json
import os

class DownloadButtonUI:
    def __init__(self, form: CheckoutUI) -> None:

        # Get the absolute path to the JSON file
        json_file_path = os.path.join("config", f"{sanitize_filename(form.payment_method_name)}.json")

        self.download_btn = st.button(
            "Save Pay Method data",
            key="save-btn",
            type="secondary",
            use_container_width=True)
        if self.download_btn:
            with open(json_file_path, "w") as f:
                f.write(f"[{json.dumps(save_pay_data(form), indent=4)}]")
            st.toast("Payment configuration saved", icon="✅")
