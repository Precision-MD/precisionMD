import streamlit as st
import os


def show_home():
    img_left, img_center, img_right = st.columns((1, 3, 1))
    with img_center:
        st.image(
            'images/full_pmd_logo_transparent.png', use_column_width=True)

    # Main content of the Home page
    st.title("Welcome to PrecisionMD!")
    st.write(
        "PrecisionMD is dedicated to advancing precision medicine through innovative technologies.")
    st.warning(
        "⚠️ Medication recommendations from PrecisionMD should be vetted by a medical professional before being prescribed.")
    st.markdown("---")  # Separator

    # FAQ section with a link
    st.subheader("Frequently Asked Questions")
    with st.expander("What is precision medicine?"):
        st.write('''
            The use of genetic profiling to optimize the therapeutic benefit of prescribed medication.
        ''')
    with st.expander("What dataset is the model trained on?"):
        st.write('''
            The model is trained on data collected from a clinical trial exploring the role of pharmacogenetics in depression medication. 
            Here's the [study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7178493/) and accompanying [data](https://data.mendeley.com/datasets/25yjwbphn4/1).
        ''')
    with st.expander("What genes does our model specialize in?"):
        st.write('''
            Currently, only the CYP2D6 gene which is responsible for metabolizing antidepressants.
        ''')
