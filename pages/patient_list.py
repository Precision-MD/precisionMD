import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy.sql import text
from streamlit_navigation_bar import st_navbar
import uuid


def show_patient_list():
    st.header("Patient List")
    # check if key exists in current session state
    if "patient_rows" not in st.session_state:
        # create key in session
        st.session_state["patient_rows"] = []

    # store all initalized patients
    patient_collection = []
    # patient_names = []

    def add_patient(patient_name):  # function to add a new patient to collection
        element_id = uuid.uuid4()  # generate a distinguishable id
        st.session_state["patient_rows"].append(
            # create unique patient rows variable
            (patient_name, str(element_id)))

    # function to generate and display new patient expander component

    def generate_patient(row_id, patient_name):
        row_container = st.empty()  # create empty container
        # separate container with columns
        patient_col = row_container.columns((15, 2))
        # define column for patient info and delete button
        patient_expander = patient_col[0].expander(f"{patient_name}")
        patient_expander.write(
            '''"Model Output Goes Here!"'''
        )
        patient_col[1].button("Delete", key=f"del_{(patient_name, row_id)}",
                              on_click=remove_patient, args=[(patient_name, row_id)])

    def remove_patient(row_id):  # function to remove an existing patient from collection
        # remove specific patient key from session
        st.session_state["patient_rows"].remove(row_id)

    # *** PATIENT LIST
    # form to create a patient
    @st.experimental_dialog("Patient Info", width="large")
    def patient_form():
        st.header("Patient List")
        # separate form fields into columns
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        # form fields
        with col1:
            name = st.text_input("Name")

        with col2:
            gender = st.text_input("Gender")

        with col3:
            age = st.text_input("Age")

        with col4:
            ethnicity = st.text_input("Ethnicity")

        with col5:
            gene_type = st.text_input("Gene Type")

        if st.button("Generate Report"):
            st.session_state.patient_form = {"gr": True,
                                             "name": name, "gender": gender, "age": age, "ethnicity": ethnicity, "gene_type": gene_type}
            st.rerun()  # rerun script to close modal

    # when add patient button is clicked
    if st.button("Add Patient"):
        patient_form()
        return

    if "patient_form" not in st.session_state:
        pass
    else:
        # check if the generate report button was clicked
        if st.session_state.patient_form["gr"] == True:
            menu = st.columns(2)
            with menu[0]:
                # add new patient to collection
                add_patient(st.session_state.patient_form["name"])
            # reset generate report key
            st.session_state.patient_form["gr"] = False

        # iterate over and generate all patients in collection
        for patient in st.session_state['patient_rows']:
            print(patient_collection)
            new_patient = generate_patient(
                patient[1], f"{patient[0]}")
            patient_collection.append(new_patient)