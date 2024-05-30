import logging

import streamlit as st
import streamlit.components.v1 as components
import validators
from io_file_validator.validator import ValidatorDataframe
from pandera.errors import SchemaError

logger = logging.getLogger(__name__)

if "panderas_url" not in st.session_state:
    st.session_state["panderas_url"] = "Unassigned"


def assign_panderas_url(panderas_url):
    if validators.url(panderas_url):
        st.success("Valid URL! Proceed.")
        st.session_state["panderas_url"] = panderas_url
    else:
        st.session_state["panderas_url"] = "Unassigned"
        st.error("Panderas URL not valid!")


def set_panderas_url_from_selectbox(standards):
    names = list(standards)
    name = st.selectbox(
        label="File standard (as defined in standards section)",
        options=(names),
    )
    # Add a button to confirm selection
    if st.button("Confirm"):
        # Check if a selection has been made
        if name:
            # Perform actions based on the selected name
            st.write("Selected name:", name)
        else:
            # Display an error message if no selection is made
            st.error("Please select a name.")
        standard_url = standards[name]
        st.success(f"Selected {name}, we will validate file against {standard_url}")
        assign_panderas_url(panderas_url=standard_url)


def run_validation(validator, uploaded_file):
    try:
        dataframe = validator.run_validation(uploaded_file=uploaded_file)
    except SchemaError as e:
        st.error(
            f"""
                Please fix file and try again!!!\n\n\n
                Validation failed with error message: {e}.
            """
        )
        return None
    return dataframe


def run_validate_file(standards: dict, validator: ValidatorDataframe = None):
    """
    standards is a key value pair of name and url
    e.g.: 'inclinometr': 'https://path/to/panderas/url"""
    if not validator:
        validator = ValidatorDataframe(url=None, file_format="csv")
    with st.sidebar:
        components.html(
            """
            <iframe src="https://github.com/sponsors/machov/button"
            title="Sponsor machov" height="32" width="114" style="border: 0;
            border-radius: 6px;"></iframe>
            """
        )

    set_panderas_url_from_selectbox(standards=standards)

    if "panderas_url" in st.session_state:

        if st.session_state["panderas_url"] is not None and st.session_state["panderas_url"] != "Unassigned":
            validator.url = st.session_state["panderas_url"]
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                dataframe = run_validation(validator=validator, uploaded_file=uploaded_file)
                if dataframe is not None:
                    st.success("Validated dataframe! Dataframe head shown below: ")
                    st.dataframe(dataframe.head())
                    st.balloons()
                    return uploaded_file
    return None


def run():
    st.set_page_config(
        page_title="Data Validator Home",
        page_icon="📊",
    )
    st.write("# Data Validation Tool! 📊")
    standards = {
        "store_schema": ("https://raw.githubusercontent.com/resilientinfrastructure/standards/main/panderas_schema.yml")
    }
    run_validate_file(standards=standards)


if __name__ == "__main__":
    run()
