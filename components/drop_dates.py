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
        # Setting up the App Title and Icon
        icon_col, title_col = st.columns([0.07, 0.93])
        title_col.title("Supremebot")

        # Get the absolute path to the icon image file
        icon_file_path = os.path.join("img", "icon.png")
        icon_col.image(icon_file_path, width=100)

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
