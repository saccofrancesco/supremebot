# Importing Libraries
import streamlit as st
from components.utils import save_pay_data
from components.checkout import CheckoutUI
import json

class DownloadButtonUI:
    def __init__(self, form: CheckoutUI) -> None:
        
        self.download_btn = st.button("Save Pay Method data", key="save-btn", type="secondary")
        if self.download_btn:
            with open("./config/pay.config.json", "w") as f:
                f.write(f"[{json.dumps(save_pay_data(form), indent=4)}]")
            st.toast("Payment configuration saved", icon="✅")
