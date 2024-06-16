import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import pages

# *** IMPORTED NAVIGATION BAR
st.set_page_config(initial_sidebar_state="collapsed")
web_pages = ["Home", "Login", "Patient List"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(
    parent_dir, "/Users/jiyapatel/new-streamlit/precisionMD/images/gene_svg.svg")
styles = {
    "nav": {
        "background-color": "#5D7298",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
        "width": "150px",
        "height": "150px"

    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "#A6B2C9",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    }
}
options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    web_pages,
    logo_path=logo_path,
    styles=styles,
    options=options,
)

functions = {
    "Login": pages.show_login,
    "Home": pages.show_home,
    "Patient List": pages.show_patient_list,
    "About Us": pages.show_about_us
}
go_to = functions.get(page)
if go_to:
    go_to()
