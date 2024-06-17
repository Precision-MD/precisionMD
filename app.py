import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import pages as pg


# *** IMPORTED NAVIGATION BAR
st.set_page_config(initial_sidebar_state="collapsed")
pages = ["Home", "Login", "Patient List"]
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
    pages,
    logo_path=logo_path,
    styles=styles,
    options=options,
)

functions = {
    "Login": pg.show_login,
    "Home": pg.show_home,
    "Patient List": pg.show_patient_list,
}
go_to = functions.get(page)
if go_to:
    go_to()
