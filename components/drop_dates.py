# Importing Libraries
import streamlit as st
from components.utils import get_drop_dates
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

class DropDatesUI:
    def __init__(self) -> None:

        # Setting up the App Title and Icon
        icon_col, title_col = st.columns([0.07, 0.93])
        title_col.title("Supremebot")
        icon_col.image("./img/icon.png", width=100)

        # Fetching the dates
        drop_dates: list = get_drop_dates()

        # Input for the user to select a valid Drop Date
        colored_header("Select a Drop Date", "", "red-80")
        add_vertical_space(1)
        self.selected_date: str = st.selectbox(
            " ", drop_dates, label_visibility="collapsed")
