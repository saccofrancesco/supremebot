# Importing Libraries
from typing import List, Dict, Union
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from components.utils import is_json_file_empty
import json
import os

class BasketUI:
    def __init__(self) -> None:
        # Get the absolute path to the JSON file
        self.json_file_path: str = os.path.join("config", "items.json")
        self.is_empty: bool = self.show_basket_content()

    def load_data_from_json(self) -> List[Dict[str, Union[str, int]]]:
        try:
            # Attempt to load data from the JSON file
            with open(self.json_file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # Handle errors when loading data
            st.error(f"Error loading data: {e}")
            return []

    def display_item(self, item: Dict[str, Union[str, int]]) -> None:
        # Display information about a single item in the basket
        col1, col2, col3, col4, col5 = st.columns([0.8, 4.5, 1, 1, 1])
        col1.image(item["image"], width=80)
        col2.markdown(f"**Name**\n\n{item['name']}")
        col3.markdown(f"**Color**\n\n{item['color']}")
        col4.markdown(f"**Size**\n\n{item['size']}")
        col5.markdown(f"**Price**\n\n{item['price']}")
        add_vertical_space(1)

    def show_basket_content(self) -> bool:
        # Load data from JSON file
        data: List[Dict[str, Union[str, int]]] = self.load_data_from_json()

        # Check if data is empty or JSON file is empty
        if not data or is_json_file_empty(self.json_file_path):
            return True  # Basket is empty

        # Display header for selected products
        colored_header("Selected Products", "", "red-80")
        add_vertical_space(1)

        # Display information for each item in the basket
        for item in data:
            self.display_item(item)

        return False  # Basket is not empty
