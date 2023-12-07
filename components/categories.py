# Importing Libraries
from streamlit_option_menu import option_menu

class CategoriesUI:
    def __init__(self) -> None:

        # Input for the user to select item types
        self.items_category: str = option_menu(
            menu_title="Select a Category",
            options=[" T-Shirts", "Accessories", "Sweatshirts", "Hats", "Jackets",
                     "Tops", "Pants", "Skate", "Bags", "Shirts"],
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
