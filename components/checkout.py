# Importing Libraries
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space


class CheckoutUI:
    def __init__(self) -> None:

        # Requesting user personal infos
        colored_header("Checkout", "", "red-80")
        add_vertical_space(1)

        # Option to load a pay config saved from previus buys
        st.subheader("Select a Pay configuration file")
        pay_config = st.file_uploader(
            " ", label_visibility="collapsed", type="JSON")

        st.subheader("Contact")
        from components.utils import get_pay_prop
        self.email: str = st.text_input(
            " ",
            value=get_pay_prop(pay_config, "email") if pay_config else "",
            label_visibility="collapsed",
            placeholder="Email")
        st.subheader("Billing / Shipping information")

        first_name_col, last_name_col = st.columns(2)
        self.name: str = first_name_col.text_input(
            " ", label_visibility="collapsed", placeholder="名",
            value=get_pay_prop(pay_config, "first_name") if pay_config else "")
        self.surname: str = last_name_col.text_input(
            " ", label_visibility="collapsed", placeholder="姓",
            value=get_pay_prop(pay_config, "last_name") if pay_config else "")

        from components.utils import prefecture_list
        self.prefecture: str = st.selectbox(
            " ", prefecture_list(), label_visibility="collapsed",
            index=prefecture_list().index(get_pay_prop(pay_config, "prefecture")) if pay_config else 0)

        self.address: str = st.text_input(
            " ", label_visibility="collapsed", placeholder="住所",
            value=get_pay_prop(pay_config, "address") if pay_config else "")
        self.buildings_name: str = st.text_input(
            " ",
            value=get_pay_prop(
                pay_config, "buildings_name") if pay_config else "",
            label_visibility="collapsed",
            placeholder="建物名、部屋番号など")

        # Reactive UI based on selected Country
        postal_code_col, city_col = st.columns(2)
        self.postal_code: str = postal_code_col.text_input(
            " ", label_visibility="collapsed", placeholder="郵便番号",
            value=get_pay_prop(pay_config, "postal_code") if pay_config else "")
        self.city: str = city_col.text_input(
            " ", label_visibility="collapsed", placeholder="市町村",
            value=get_pay_prop(pay_config, "city") if pay_config else "")

        self.phone: str = st.text_input(
            " ",
            value=get_pay_prop(pay_config, "phone") if pay_config else "",
            label_visibility="collapsed",
            placeholder="電話番号")
        st.subheader("Credit Card Information")
        self.card_number: str = st.text_input(
            " ", label_visibility="collapsed", placeholder="Card Number",
            value=get_pay_prop(pay_config, "card_number") if pay_config else "")
        expiration_year_col, expiration_month_col, cvv_col = st.columns(3)

        from components.utils import get_card_exp_years
        self.expiration_year: str = expiration_year_col.selectbox(
            " ", get_card_exp_years(), label_visibility="collapsed", placeholder="Exp. year",
            index=get_card_exp_years().index(get_pay_prop(pay_config, "expiration_year")) if pay_config else 0)

        from components.utils import months_in_numbers
        self.expiration_month: str = expiration_month_col.selectbox(
            " ", months_in_numbers(int(self.expiration_year)),
            index=months_in_numbers(int(self.expiration_year)).index(
                get_pay_prop(pay_config, "expiration_month")) if pay_config else 0,
            label_visibility="collapsed",
            placeholder="Exp. month")
        self.cvv: int = cvv_col.text_input(
            " ", label_visibility="collapsed", placeholder="CVV",
            value=get_pay_prop(pay_config, "cvv") if pay_config else "")
        name_on_card_col, self.save_data_col = st.columns([6, 1])
        self.name_on_card: str = name_on_card_col.text_input(
            " ", label_visibility="collapsed", placeholder="カード名義",
            value=get_pay_prop(pay_config, "name_on_card") if pay_config else "")
