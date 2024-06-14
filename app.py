import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy.sql import text
import uuid

# *** DATABASE
# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.connection('patients_db', type='sql')

# Insert some data with conn.session.
with conn.session as s:
    s.execute(text('CREATE TABLE IF NOT EXISTS patients (id INTEGER, name TEXT);'))
    s.execute(text('DELETE FROM patients;'))
    patients = {1000: 'Emily Thompson', 1001: 'David Lee'}
    for k in patients:
        s.execute(
            text('INSERT INTO patients (id, name) VALUES (:id, :name);'),
            params=dict(id=k, name=patients[k])
        )
    s.commit()

# *** NAVIGATION BAR
# horizontal nav-bar
selected = option_menu(
    menu_title=None,
    options=['Home', 'Patient List', 'FAQ'],
    icons=['house', 'person-lines-fill', 'question-circle'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal',
)

# *** HOME
if selected == 'Home':
    st.title("Home")

# check if key exists in current session state
if "patient_rows" not in st.session_state:
    # create key in session
    st.session_state["patient_rows"] = []

# store all initalized patients
patient_collection = []


def add_patient():  # function to add a new patient to collection
    element_id = uuid.uuid4()  # generate a distinguishable id
    st.session_state["patient_rows"].append(
        str(element_id))  # create unique patient rows variable


# function to generate and display new patient expander component
def generate_patient(row_id):
    row_container = st.empty()  # create empty container
    # separate container with columns
    patient_col = row_container.columns((15, 2))
    # define column for patient info and delete button
    patient_expander = patient_col[0].expander("Patient Name")
    patient_expander.write(
        '''"Model Output Goes Here!"'''
    )
    patient_col[1].button("Delete", key=f"del_{row_id}",
                          on_click=remove_patient, args=[row_id])


def create_patient():
    # loop over and initialize all patients in the session
    for patient in st.session_state['patient_rows']:
        new_patient = generate_patient(patient)
        patient_collection.append(new_patient)

    menu = st.columns(2)
    with menu[0]:
        add_patient()


def remove_patient(row_id):  # function to remove an existing patient from collection
    # remove specific patient key from session
    st.session_state["patient_rows"].remove(str(row_id))


# *** PATIENT LIST
if selected == 'Patient List':

    # form to create a patient
    @st.experimental_dialog("Patient Info", width="large")
    def patient_form():

        st.write(f"Patients")

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
            st.session_state.patient_form = {
                "name": name, "gender": gender, "age": age, "ethnicity": ethnicity, "gene_type": gene_type}
            st.rerun()  # rerun script to close modal

    st.title("Patient List")  # page title
    if st.button("Add Patient"):  # when add patient button is clicked
        patient_form()
    else:
        create_patient()  # create a new patient expander component

# *** FAQ
if selected == 'FAQ':
    st.title("FAQ")
