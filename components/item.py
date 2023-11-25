# Importing Libraries
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from components.utils import is_item_in_basket, add_to_basket, remove_from_basket
from components.utils import get_info_for_item, fetch_items
from streamlit_extras.colored_header import colored_header


class ItemUI:
    def __init__(self, category: str, dates: str) -> None:

        if category != "None":
            items: dict = fetch_items(dates, category)
            colored_header(f"{category} Products", "", "red-80")
            add_vertical_space(1)

            # For each item, show the product card
            for item in items:

                # Creating Items attributes
                self.name = item
                self.image = items[self.name]["image"]
                self.price = items[self.name]['price']

                image_col, info_col, buttons_col = st.columns([1, 1.5, 2.5])
                image_col.image(self.image, width=220)
                info_col.markdown(f"**Item Name:** {self.name}")
                info_col.markdown(f"**Price:** {self.price}")
                if not is_item_in_basket(self.name):
                    if items[self.name]["colors"]:
                        self.color: str = buttons_col.radio(
                            "Colors:", items[self.name]["colors"], key=f"{self.name}_color", horizontal=True)
                    else:
                        buttons_col.markdown("**Colors:** None")
                        self.color: str = "None"

                    if items[self.name]["category"] in [
                        "t-shirts",
                        "sweatshirts",
                        "jackets",
                        "tops-sweaters",
                        "pants",
                            "shirts"]:

                        # Generate a unique key for the selectbox based on item
                        # name
                        size_key: str = f"{self.name}_size"
                        self.size: str = buttons_col.selectbox(
                            "Sizes:", ["Small", "Medium", "Large", "XLarge"], key=size_key)
                    else:
                        self.size: str = "None"

                    # Generate a unique key for the button based on item name
                    self.add_key: str = f"{self.name}_add_to_basket"

                    # Use the unique key for the button
                    buttons_col.button(
                        "Add to basket",
                        key=self.add_key,
                        on_click=add_to_basket,
                        args=(
                            self.image,
                            self.price,
                            self.name,
                            self.color,
                            self.size,
                            items[self.name]["category"]))
                else:
                    self.remove_key: str = f"{self.name}_remove_from_basket"
                    info_col.markdown(
                        f'**Color:** {get_info_for_item(self.name, "color")}')
                    info_col.markdown(
                        f'**Size:** {get_info_for_item(self.name, "size")}')
                    info_col.button(
                        "Remove from basket",
                        key=self.remove_key,
                        type="primary",
                        on_click=remove_from_basket,
                        args=(
                            self.name,
                        ))
                add_vertical_space(2)
