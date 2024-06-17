import streamlit as st
import os

def show_home():
    st.set_page_config(page_title="PrecisionMD Home", page_icon="🧬")

    # Define paths
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(parent_dir, "images", "gene_svg.svg")  # Adjust as per your actual folder structure

    # Main content of the Home page
    st.title("Welcome to PrecisionMD!")
    st.write("PrecisionMD is dedicated to advancing precision medicine through innovative technologies.")

    st.markdown("---")  # Separator

    # FAQ section with a link
    st.subheader("Frequently Asked Questions")
    st.write("Explore our [FAQ page](https://www.example.com/faq) for more information.")

    # Example navigation links
    if st.button("Home"):
        st.write("You are on the Home page.")
    if st.button("Login"):
        st.write("Navigate to the Login page.")
    if st.button("Patient List"):
        st.write("Navigate to the Patient List page.")

    # Display logo
    if os.path.exists(logo_path):
        st.image(logo_path, caption='PrecisionMD Logo', use_column_width=True)
    else:
        st.write("Logo not found.")

