# Importing Libraries
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from components.zones import ZONES
import os

class CheckoutUI:
    def __init__(self) -> None:

        # Requesting user personal infos
        colored_header("Checkout", "", "red-80")
        add_vertical_space(1)

        # Option to load a pay config saved from previus buys
        path: str = os.path.join("config", "pay.json")
        pay_config: bool = os.path.exists(path)

        # Requesting contact email
        st.subheader("Contact")
        from components.utils import get_pay_prop
        self.email: str = st.text_input(
            " ",
            value=get_pay_prop("email") if pay_config else "",
            label_visibility="collapsed",
            placeholder="Email")

        # Splitting the form in two columns
        col1, self.col2 = st.columns(2)

        # Filling the first column
        col1.subheader("Shipping Info")
        from components.utils import country_list
        self.country: str = col1.selectbox(
            " ", country_list(), label_visibility="collapsed", index=country_list().index(
                get_pay_prop("country")) if pay_config else 0)
        first_name_col, last_name_col = col1.columns(2)
        self.name: str = first_name_col.text_input(
            " ", label_visibility="collapsed", placeholder="Name",
            value=get_pay_prop("first_name") if pay_config else "")
        self.surname: str = last_name_col.text_input(
            " ", label_visibility="collapsed", placeholder="Surname",
            value=get_pay_prop("last_name") if pay_config else "")
        self.address: str = col1.text_input(
            " ", label_visibility="collapsed", placeholder="Address",
            value=get_pay_prop("address") if pay_config else "")

        # Reactive UI based on selected Country
        if self.country in [country for country in ZONES.keys()]:
            postal_code_col, city_col, zone_col = col1.columns(3)
            self.postal_code: str = postal_code_col.text_input(
                " ", label_visibility="collapsed", placeholder="Postal Code",
                value=get_pay_prop("postal_code") if pay_config else "")
            self.city: str = city_col.text_input(
                " ", label_visibility="collapsed", placeholder="City",
                value=get_pay_prop("city") if pay_config else "")

            from components.utils import country_zones
            self.zone: str = zone_col.selectbox(
                " ", country_zones(
                    self.country), label_visibility="collapsed", index=country_zones(
                    self.country).index(
                    get_pay_prop("zone")) if pay_config and get_pay_prop("zone") != "None" else 0)
        else:
            postal_code_col, city_col = col1.columns(2)
            self.postal_code: str = postal_code_col.text_input(
                " ", label_visibility="collapsed", placeholder="Postal Code",
                value=get_pay_prop("postal_code") if pay_config else "")
            self.city: str = city_col.text_input(
                " ", label_visibility="collapsed", placeholder="City",
                value=get_pay_prop("city") if pay_config else "")

        self.phone: str = col1.text_input(
            " ",
            value=get_pay_prop("phone") if pay_config else "",
            label_visibility="collapsed",
            placeholder="Phone")

        # Filling second column
        self.col2.subheader("Credit Card Info")
        self.card_number: str = self.col2.text_input(
            " ", label_visibility="collapsed", placeholder="Card Number",
            value=get_pay_prop("card_number") if pay_config else "")
        expiration_year_col, expiration_month_col = self.col2.columns(2)

        from components.utils import get_card_exp_years
        self.expiration_year: str = expiration_year_col.selectbox(
            " ",
            get_card_exp_years(),
            label_visibility="collapsed",
            placeholder="Exp. year",
            index=get_card_exp_years().index(
                get_pay_prop("expiration_year")) if pay_config else 0)

        from components.utils import months_in_numbers
        self.expiration_month: str = expiration_month_col.selectbox(
            " ",
            months_in_numbers(
                int(
                    self.expiration_year)),
            index=months_in_numbers(
                int(
                    self.expiration_year)).index(
                        get_pay_prop("expiration_month")) if pay_config else 0,
            label_visibility="collapsed",
            placeholder="Exp. month")
        self.cvv: int = self.col2.text_input(
            " ", label_visibility="collapsed", placeholder="CVV",
            value=get_pay_prop("cvv") if pay_config else "")
        self.name_on_card: str = self.col2.text_input(
            " ", label_visibility="collapsed", placeholder="Name on Card",
            value=get_pay_prop("name_on_card") if pay_config else "")
        self.save_pay_method_col, self.buy_col = self.col2.columns(2)
