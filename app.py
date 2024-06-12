import streamlit as st
from streamlit_option_menu import option_menu

# horizontal nav-bar
selected = option_menu(
    menu_title=None,
    options=['Home', 'Patient List', 'FAQ'],
    icons=['house', 'person-lines-fill', 'question-circle'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal',
)

# different nav bar pages
if selected == 'Home':
    st.title("Home")
if selected == 'Patient List':
    st.title("Patient List")
if selected == 'FAQ':
    st.title("FAQ")
