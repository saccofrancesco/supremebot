# Importing Libraries
import streamlit as st
from components.utils import get_drop_dates
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import os
from typing import List, Optional

class DropDatesUI:
    def __init__(self) -> None:
        self.setup_ui()

    def setup_ui(self) -> None:
        st.title("Supremebot")

        try:
            # Fetching the dates
            drop_dates: List[str] = self.get_drop_dates()

            # Input for the user to select a valid Drop Date
            colored_header("Select a Drop Date", "", "red-80")
            add_vertical_space(1)
            self.selected_date: Optional[str] = st.selectbox(
                " ", drop_dates, label_visibility="collapsed")
        except Exception as e:
            st.error(f"Error fetching drop dates: {e}")

    @staticmethod
    def get_drop_dates() -> List[str]:
        # Fetch drop dates
        return get_drop_dates() or []  # Return an empty list if no dates are available
