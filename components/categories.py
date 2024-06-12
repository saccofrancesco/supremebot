# Importing Libraries
from typing import List
from streamlit_option_menu import option_menu

class CategoriesUI:
    """
    A class to represent the Categories User Interface in a Streamlit application.

    Attributes:
        CATEGORIES (List[str]): A list of available categories.
        items_category (str): The category selected by the user.
    """
    # Define a list of available categories
    CATEGORIES: List[str] = [
        "T-Shirts", "Accessories", "Sweatshirts", "Hats", "Jackets",
        "Tops", "Pants", "Skate", "Bags", "Shirts"
    ]

    def __init__(self) -> None:
        """
        Initializes the CategoriesUI instance by creating the category selection menu.
        """
        # Input for the user to select item types
        self.items_category: str = self.create_category_menu()

    def create_category_menu(self) -> str:
        """
        Creates a dropdown menu for selecting a category.

        Returns:
            str: The selected category.
        """
        # Create a dropdown menu for selecting a category
        return option_menu(
            menu_title="Select a Category",
            options=self.CATEGORIES,
            default_index=0,
            menu_icon="list-task",
            icons=None,
            orientation="horizontal",
            styles={
                "container": {"font-family": "sans-serif"},
                "menu-title": {"font-weight": "bold"},
                "separator": {"color": "solid red"},
                "icon": {"display": "none"}
            }
        )
