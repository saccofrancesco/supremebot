# Importing Libraries
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from components.utils import is_json_file_empty
import json

class BasketUI:
    def __init__(self) -> None:

        # Showing the basket content if not empty
        if not is_json_file_empty("./config/items.json"):
            self.is_empty = False
            colored_header(":page_with_curl: Selected Products", "")
            add_vertical_space(1)
            with open("./config/items.json", "r") as file:
                data: str = json.load(file)
            total: int = 0
            for item in data:
                try:
                    total += int(item['price'].replace("$", ""))
                except ValueError:
                    pass
                col1, col2, col3, col4, col5 = st.columns([0.8, 4.5, 1, 1, 1])
                col1.image(item["image"], width=80)
                col2.markdown(f"**Name:**\n\n{item['name']}")
                col3.markdown(f"**Color:**\n\n{item['color']}")
                col4.markdown(f"**Size:**\n\n{item['size']}")
                col5.markdown(f"**Price:**\n\n{item['price']}")
                add_vertical_space(1)
            col5.divider()
            col5.markdown(f"**Total:**\n\n${total}")
        else:
            self.is_empty = True
