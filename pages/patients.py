import streamlit as st
import uuid
import time
import pickle
import sklearn
import numpy as np
import requests
import json
import pandas as pd
import plotly.express as px


def open_fda_api(medication_name):  # makes call to openFDA Drugs API
    url = "https://api.fda.gov/drug/event.json?search=patient.drug.openfda.brand_name:" + \
        medication_name + "&count=patient.reaction.reactionmeddrapt.exact"
    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        data = json.loads(response.text)
        reactions = []
        counts = []
        # extract top 5 side effects reported to be experienced by patients
        i = 0
        for reaction in data['results']:
            if i >= 5:
                break
            extracted_reaction = reaction['term']
            reactions.append(extracted_reaction)

            extracted_reaction_count = reaction['count']
            counts.append(extracted_reaction_count)
            i += 1

        if data.get('results'):
            return (reactions, counts)
        else:
            print(f"No results found for '{medication_name}'.")

    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed. {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Unable to parse JSON response. {e}")


def format_user_input(patient_form_filled):  # format user input into a form
    # age, gender, mdd, severe, recurrent, psychotic, B, L, O/U, W, CT: abnormal, EG: normal, TL: extreme
    user_input = []

    # age
    regular_age = int(float(patient_form_filled["age"]))
    normalized_age = (regular_age - 18) / (85 - 18)
    # add age to model input
    user_input.append(normalized_age)

    # gender
    if patient_form_filled["gender"] == "Male":
        user_input.append(1)
    else:
        user_input.append(0)

    # diagnosis (mdd, severe, recurrent, psychotic)
    diagnosis_list = [False, False, False, False]
    for diagnosis in patient_form_filled["diagnosis"]:
        if diagnosis == 'MDD':
            diagnosis_list[0] = True
        elif diagnosis == 'Severe':
            diagnosis_list[1] = True
        elif diagnosis == 'Recurrent':
            diagnosis_list[2] = True
        elif diagnosis == 'Psychotic':
            diagnosis_list[3] = True

    # add diagnosis to model input
    for diagnosis in diagnosis_list:
        user_input.append(diagnosis)

    # ethnicity (B, L, O/U, W)
    ethnicity_list = [False, False, False, False]
    if patient_form_filled["ethnicity"] == 'Black':
        ethnicity_list[0] = True
    elif patient_form_filled["ethnicity"] == 'Latino':
        ethnicity_list[1] = True
    elif patient_form_filled["ethnicity"] == 'Other/Unknown':
        ethnicity_list[2] = True
    elif patient_form_filled["ethnicity"] == 'White':
        ethnicity_list[3] = True

    # add ethnicity to model input
    for ethnicity in ethnicity_list:
        user_input.append(ethnicity)

    # gene type (CT: abnormal, EG: normal, TL: extreme)
    gene_list = [False, False, False]
    for gene in patient_form_filled["gene_type"]:
        if patient_form_filled["gene_type"] == 'Abnormal':
            gene_list[0] = True
        elif patient_form_filled["gene_type"] == 'Normal':
            gene_list[1] = True
        elif patient_form_filled["gene_type"] == 'Extreme':
            gene_list[2] = True

    # add gene to model input
    for gene in gene_list:
        user_input.append(gene)

    return user_input


def pickle_model(formatted_user_input):  # interact with model and return prediction
    # open and load pickle file
    with open('model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)

    test_subject = np.array([formatted_user_input])
    test_subject.reshape(1, -1)

    prediction = loaded_model.predict(test_subject)

    return prediction


def decode_medication(prediction_list):  # return decoded medication predictions
    # letter coded medication dictionary
    med_dict = {'A': 'AMITRIPTYLINE', 'B': 'ARIPIPRAZOLE', 'C': 'ASENAPINE',
                'D': 'BUPROPION', 'E': 'CHLORPROMAZINE', 'F': 'CITALOPRAM',
                'G': 'CLOMIPRAMINE', 'H': 'CLONIDINE', 'I': 'DOXEPIN',
                'J': 'DULOXETINE', 'K': 'ESCITALOPRAM', 'L': 'FLUOXETINE',
                'M': 'FLUPHENAZINE', 'N': 'FLUVOXAMINE', 'O': 'GUANFACINE',
                'P': 'HALOPERIDOL', 'Q': 'IMIPRAMINE', 'R': 'LITHIUM CARBONATE',
                'S': 'METHYLPHENIDATE', 'T': 'MIRTAZAPINE', 'U': 'NORTRIPTYLINE',
                'V': 'OLANZAPINE', 'W': 'PALIPERIDONE', 'X': 'PERPHENAZINE',
                'Y': 'QUETIAPINE', 'Z': 'RISPERIDONE', 'AA': 'SERTRALINE',
                'AB': 'TRAZODONE', 'AC': 'VENLAFAXINE', 'AD': 'ZIPRASIDONE'
                }

    first_med = prediction_list[0][0]
    second_med = prediction_list[0][1]

    decoded_rec_one = (med_dict[first_med]).capitalize()
    decoded_rec_two = (med_dict[second_med]).capitalize()

    decoded_prediction = [decoded_rec_one, decoded_rec_two]
    return decoded_prediction


def show_patients():
    st.header("Patient List")

    # check if key exists in current session state
    if "patient_rows" not in st.session_state:
        # create key in session
        st.session_state["patient_rows"] = []

    # store all initalized patients
    patient_collection = []

    def add_patient(patient_form_filled):  # function to add a new patient to collection
        element_id = uuid.uuid4()  # generate a distinguishable id
        st.session_state["patient_rows"].append(
            # create unique patient rows variable
            (patient_form_filled, str(element_id)))

    # function to generate and display new patient expander component
    def generate_patient(patient_form_filled, row_id):
        row_container = st.empty()  # create empty container
        # separate container with columns
        patient_col = row_container.columns((15, 2))
        # define column for patient info and delete button
        name_patient = patient_form_filled["name"]
        patient_expander = patient_col[0].expander(name_patient)

        # *** TRIGGER INTERACTION WITH MODEL
        # format user input for model intake
        user_input = format_user_input(patient_form_filled)
        print(user_input)
        # retrieve mdeication predictions from model
        coded_prediction = pickle_model(user_input)
        # decode letter coded medication model predicts
        decoded_prediction = decode_medication(coded_prediction)
        print(decoded_prediction)

        with patient_expander:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f'''
                    **Gender:** {patient_form_filled["gender"]} \n
                    **Age:** {patient_form_filled["age"]} \n
                    **Ethnicity:** {patient_form_filled["ethnicity"]} \n
                    **Diagnosis:** {patient_form_filled["diagnosis"]} \n
                    **Gene Type:** {patient_form_filled["gene_type"]} \n
                ''')
            with col2:
                st.markdown(
                    f'''
                    **Recommended Medications:**
                    1. {decoded_prediction[0]}
                    2. {decoded_prediction[1]}
                    '''
                )
            st.markdown("---")  # Separator
            # plot reactions graph by triggering API call on predicted drugs
            drug_one_reactions = open_fda_api(decoded_prediction[0])
            drug_two_reactions = open_fda_api(decoded_prediction[1])

            st.subheader("Reported Drug Reactions")
            tab1, tab2 = st.tabs(
                [f"{decoded_prediction[0]} Reactions", f"{decoded_prediction[1]} Reactions"])
            if len(drug_one_reactions) != 0:
                df1 = pd.DataFrame(
                    {'Reactions': drug_one_reactions[0], 'Count': drug_one_reactions[1]})

                fig1 = px.bar(
                    df1,
                    x="Reactions",
                    y="Count",
                    color="Count",
                    color_continuous_scale="blues",
                    range_color=[min(df1['Count'] - 1000), max(df1['Count'])],
                )
                with tab1:
                    st.plotly_chart(fig1, theme="streamlit",
                                    use_container_width=True)
            else:
                with tab1:
                    st.write(f"No results found for {decoded_prediction[0]}.")

            if len(drug_two_reactions) != 0:
                df2 = pd.DataFrame(
                    {'Reactions': drug_two_reactions[0], 'Count': drug_two_reactions[1]})
                fig2 = px.bar(
                    df2,
                    x="Reactions",
                    y="Count",
                    color="Count",
                    color_continuous_scale="blues",
                    range_color=[min(df2['Count']) - 1000, max(df2['Count'])]
                )
                with tab2:
                    st.plotly_chart(fig2, theme="streamlit",
                                    use_container_width=True)
            else:
                with tab2:
                    st.write(f"No results found for {decoded_prediction[1]}.")

        patient_col[1].button("Delete", key=f"del_{(patient_form_filled, row_id)}",
                              on_click=remove_patient, args=[(patient_form_filled, row_id)])

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
            gender = st.selectbox(
                "Gender",
                ("Female", "Male"))
        with col3:
            age = st.text_input("Age")
        with col4:
            ethnicity = st.selectbox(
                "Ethnicity",
                ("White", "Black", "Latino", "Other/Unknown"))
        with col5:
            diagnosis = st.multiselect(
                "Diagnosis",
                ["MDD", "Severe", "Recurrent", "Psychotic"])
        with col6:
            gene_type = st.selectbox(
                "Gene Type",
                ("Normal", "Abnormal", "Extreme"))

        if st.button("Generate Report"):
            st.session_state.patient_form = {"gr": True, "name": name, "gender": gender,
                                             "diagnosis": diagnosis, "ethnicity": ethnicity, "gene_type": gene_type, "age": age
                                             }
            # filler loading flow
            with st.status("Generating Report...", expanded=True):
                st.write("Running Model...")
                time.sleep(2)
                st.write("Recommending Medication...")
                time.sleep(1)
                st.write("Process Complete...")
                time.sleep(1)
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

                add_patient(st.session_state.patient_form)
            # reset generate report key
            st.session_state.patient_form["gr"] = False

        # iterate over and generate all patients in collection
        for patient in st.session_state['patient_rows']:
            new_patient = generate_patient(patient[0],
                                           patient[1])
            patient_collection.append(new_patient)
