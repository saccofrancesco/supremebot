# Importing Libraries
import streamlit as st
from components.utils import get_drop_dates
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from typing import List, Optional

class DropDatesUI:
    """
    A class to represent the Drop Dates User Interface in a Streamlit application.

    Attributes:
        selected_date (Optional[str]): The selected drop date by the user.
    """
    def __init__(self) -> None:
        """
        Initializes the DropDatesUI instance by setting up the user interface to select drop dates.
        """
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Sets up the user interface to display drop dates and allow the user to select one.
        """
        st.title("Supremebot")

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
        """
        Static method to fetch drop dates from a data source.

        Returns:
            List[str]: A list of drop dates.
        """
        # Fetch drop dates
        return get_drop_dates() or []  # Return an empty list if no dates are available
