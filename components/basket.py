# Importing Libraries
from typing import List, Dict, Union
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from components.utils import is_json_file_empty
import json
import os

class BasketUI:
    """
    A class to represent the Basket User Interface in a Streamlit application.

    Attributes:
        json_file_path (str): Path to the JSON file containing basket items.
        is_empty (bool): Indicates if the basket is empty.
    """
    def __init__(self) -> None:
        """
        Initializes the BasketUI instance by setting the JSON file path and checking if the basket is empty.
        """
        # Get the absolute path to the JSON file
        self.json_file_path: str = os.path.join("config", "items.json")
        self.is_empty: bool = self.show_basket_content()

    def load_data_from_json(self) -> List[Dict[str, Union[str, int]]]:
        """
        Loads data from the JSON file.

        Returns:
            List[Dict[str, Union[str, int]]]: A list of dictionaries containing item details.
            Returns an empty list if the file is not found or cannot be parsed.
        """
        try:
            # Attempt to load data from the JSON file
            with open(self.json_file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # Handle errors when loading data
            st.error(f"Error loading data: {e}")
            return []

    def display_item(self, item: Dict[str, Union[str, int]]) -> None:
        """
        Displays information about a single item in the basket.

        Args:
            item (Dict[str, Union[str, int]]): A dictionary containing item details.
        """
        # Display information about a single item in the basket
        col1, col2, col3, col4, col5 = st.columns([0.8, 4.5, 1, 1, 1])
        col1.image(item["image"], width=80)
        col2.markdown(f"**Name**\n\n{item['name']}")
        col3.markdown(f"**Color**\n\n{item['color']}")
        col4.markdown(f"**Size**\n\n{item['size']}")
        col5.markdown(f"**Price**\n\n{item['price']}")
        add_vertical_space(1)

    def show_basket_content(self) -> bool:
        """
        Displays the basket content and returns whether the basket is empty.

        Returns:
            bool: True if the basket is empty, False otherwise.
        """
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
