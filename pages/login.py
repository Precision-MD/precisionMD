import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy.sql import text
from streamlit_navigation_bar import st_navbar
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
import hmac


def show_login():
    st.header("Login")

    def check_password():
        """Returns `True` if the physician had a correct password."""

        def login_form():
            """Form with widgets to collect physician information"""
            with st.form("Credentials"):
                st.text_input("Physician ID", key="physician_id")
                st.text_input("Password", type="password", key="password")
                st.form_submit_button("Log in", on_click=password_entered)

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if st.session_state["physician_id"] in st.secrets[
                "passwords"
            ] and hmac.compare_digest(
                st.session_state["password"],
                st.secrets.passwords[st.session_state["physician_id"]],
            ):
                st.session_state["password_correct"] = True
                # Don't store the physician_id or password.
                del st.session_state["password"]
                del st.session_state["physician_id"]
            else:
                st.session_state["password_correct"] = False

        # Return True if the physician_id + password is validated.
        if st.session_state.get("password_correct", False):
            return True

        # Show inputs for physician_id + password.
        login_form()
        if "password_correct" in st.session_state:
            st.error("Physician not known or password incorrect")
        return False

    if not check_password():
        st.stop()

    # Main Streamlit app starts here
    st.success("Successful Login")
    # st.write("Here goes your normal Streamlit app...")
    # st.button("Click me")
