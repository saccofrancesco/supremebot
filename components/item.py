# Importing Libraries
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from components.utils import is_item_in_basket, add_to_basket, remove_from_basket
from components.utils import get_info_for_item, fetch_items
from typing import List, Dict


class ItemUI:
    """
    A class to represent each Item inside the Interface in a Streamlit application.
    """

    def __init__(self, category: str, dates: str) -> None:
        """
        Initializes the ItemUI instance by rendering item cards based on the given category and dates.

        Args:
            category (str): The category of items to display.
            dates (str): The dates associated with the items.
        """
        self.render_item_cards(category, dates)

    @staticmethod
    def render_item_cards(category: str, dates: str) -> None:
        """
        Renders item cards for the specified category and dates.

        Args:
            category (str): The category of items to display.
            dates (str): The dates associated with the items.
        """
        items: Dict[str, Dict[str, str]] = fetch_items(dates, category)
        add_vertical_space(1)

        for item_name, item_info in items.items():
            image_col, info_col, buttons_col = st.columns([1, 1.5, 2.5])

            image_col.image(item_info["image"], width=220)
            info_col.markdown(f"**Item Name:** [{item_name}]({item_info['link']})")
            info_col.markdown(f"**Price:** {item_info['price']}")

            if not is_item_in_basket(item_name):
                ItemUI.render_item_not_in_basket(item_name, item_info, buttons_col)
            else:
                ItemUI.render_item_in_basket(item_name, info_col)

            add_vertical_space(2)

    @staticmethod
    def render_item_not_in_basket(
        item_name: str, item_info: Dict[str, str], buttons_col
    ) -> None:
        """
        Renders the UI elements for an item that is not currently in the basket.

        Args:
            item_name (str): The name of the item.
            item_info (Dict[str, str]): Information about the item.
            buttons_col: The column in which to render the buttons.
        """
        if item_info["colors"]:
            color: str = buttons_col.radio(
                "Colors", item_info["colors"], key=f"{item_name}_color", horizontal=True
            )
        else:
            buttons_col.markdown("**Colors** None")
            color = "None"

        size_options: List[str] = (
            ["None"]
            if item_info["category"]
            not in [
                "t-shirts",
                "sweatshirts",
                "jackets",
                "tops-sweaters",
                "pants",
                "shirts",
            ]
            else ["Small", "Medium", "Large", "XLarge"]
        )
        size: str = buttons_col.selectbox(
            "Sizes", size_options, key=f"{item_name}_size"
        )

        add_key: str = f"{item_name}_add_to_basket"
        buttons_col.button(
            "Add to basket",
            key=add_key,
            on_click=add_to_basket,
            args=(
                item_info["image"],
                item_info["price"],
                item_name,
                color,
                size,
                item_info["category"],
            ),
        )

    @staticmethod
    def render_item_in_basket(item_name: str, info_col) -> None:
        """
        Renders the UI elements for an item that is currently in the basket.

        Args:
            item_name (str): The name of the item.
            info_col: The column in which to render the item information.
        """
        remove_key: str = f"{item_name}_remove_from_basket"
        info_col.markdown(f'**Color:** {get_info_for_item(item_name, "color")}')
        size_info: str = get_info_for_item(item_name, "size")
        if size_info != "None":
            info_col.markdown(f"**Size:** {size_info}")
        info_col.button(
            "Remove from basket",
            key=remove_key,
            type="primary",
            on_click=remove_from_basket,
            args=(item_name,),
        )
