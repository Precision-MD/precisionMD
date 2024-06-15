import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy.sql import text
from streamlit_navigation_bar import st_navbar
import uuid
import os
import pages as pg

# # *** DATABASE
# # Create the SQL connection to pets_db as specified in your secrets file.
# conn = st.connection('patients_db', type='sql')

# # Insert some data with conn.session.
# with conn.session as s:
#     s.execute(text('CREATE TABLE IF NOT EXISTS patients (id INTEGER, name TEXT);'))
#     s.execute(text('DELETE FROM patients;'))
#     patients = {1000: 'Emily Thompson', 1001: 'David Lee'}
#     for k in patients:
#         s.execute(
#             text('INSERT INTO patients (id, name) VALUES (:id, :name);'),
#             params=dict(id=k, name=patients[k])
#         )
#     s.commit()

# *** IMPORTED NAVIGATION BAR


st.set_page_config(initial_sidebar_state="collapsed")
pages = ["Home", "Login", "Patient List", "Physician Guide", "FAQ"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "gene_svg.svg")
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
    "Physician Guide": pg.show_physician_guide
}
go_to = functions.get(page)
print(go_to)
if go_to:
    go_to()
