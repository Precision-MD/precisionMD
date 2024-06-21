# PrecisionMD
## Project Description
PrecisionMD is a software that utilizes a SVM machine learning model to create a personalized medicine tool for doctors. For a patient diagnosed with depression, it predicts the top two most effective antidepressants based on their genetic makeup and demographics, to maximize treatment success rates.

## Prototype Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://precisionmd.streamlit.app/)

## Usage 
Navigate to the Patients page and click on the "Add Patient" button to generate a new patient entry.
<img width="1197" alt="image" src="https://github.com/Precision-MD/precisionMD/assets/128255337/55a39deb-bade-4e50-b19b-e29ed4f58d3f">

Input the patient's information and click the "Generate Report" button to see the top two recommended medications and associated top 5 drug reactions reported to the FDA.

[![Watch the video](images/full_pmd_logo.png)](https://www.youtube.com/watch?v=Jp51wBdoBf8)

## Installation Instructions:
### Run it Locally
```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```


