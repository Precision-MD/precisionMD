import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy.sql import text
from streamlit_navigation_bar import st_navbar
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate


def show_login():
    st.header("Login")
