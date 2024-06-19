import streamlit as st


def show_home():
    # css styling
    center_align_css = """
    <style>
        .title {
            text-align: center;
            font-size: 40px;  # Adjust font size as needed
        }
    </style>
    """
    img_left, img_center, img_right = st.columns((1, 4, 1))

    with img_center:

        # Main content of the Home page
        st.image(
            'images/cropped_logo.png')
        st.markdown(center_align_css, unsafe_allow_html=True)
        st.markdown("<h1 class='title'>Welcome to PrecisionMD!</h1>",
                    unsafe_allow_html=True)
        st.markdown(
            "PrecisionMD is dedicated to advancing precision medicine through innovative technologies.", unsafe_allow_html=True)
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
