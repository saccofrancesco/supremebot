# Importing Libraries
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space


class CategoriesUI:
    def __init__(self) -> None:

        # Input for the user to select item types
        colored_header("Select a Category", "", "red-80")
        add_vertical_space(1)
        self.items_category: str = st.radio(" ",
                                            ["None",
                                             "T-Shirts",
                                             "Accessories",
                                             "Sweatshirts",
                                             "Hats",
                                             "Jackets",
                                             "Tops-Sweaters",
                                             "Pants",
                                             "Skate",
                                             "Shirts"],
                                            label_visibility="collapsed")
