import streamlit as st
import streamlit.components.v1 as components


def add_instructions():
    st.markdown(
        """
        ## Instructions
        """
    )
    st.markdown("""### Step 1: Select File Format""")
    st.markdown("""Choose the file format you want to ingest.""")
    st.markdown("""### Step 2: Provide Panderas Schema URL""")
    st.markdown(
        """
        [Go to Pandera documentation](https://pandera.readthedocs.io/en/stable/index.html)
        """
    )
    st.markdown(
        """
        [Create Pandera Yaml](https://pandera.readthedocs.io/en/stable/reference/generated/pandera.io.to_yaml.html)
        """
    )
    st.markdown(
        """
        Upload a raw file in the internet
        """
    )
    st.markdown(
        """
        Enter the URL to the Panderas schema you want to use for validation,
        e.g.
        "https://raw.githubusercontent.com/resilientinfrastructure/standards/main/panderas_schema.yml".
        """
    )
    st.markdown(
        """
        ### Step 3: Submit and Validate
        """
    )
    st.markdown(
        """Hit that submit button and let streamlit-pandera work its magic!
        Your data will be validated against the specified schema in no time.
        """
    )
    st.markdown(
        """
        [Go to Demo](https://youtu.be/9Ry_A9LgrbQ)
        """
    )


st.set_page_config(page_title="Instructions", page_icon="🌍")
st.markdown("# Instructions")
st.sidebar.header("Instructions")
with st.sidebar:
    components.html(
        """
        <iframe src="https://github.com/sponsors/machov/button"
        title="Sponsor machov"
        height="32"
        width="114"
        style="border: 0;
        border-radius: 6px;"></iframe>
        """
    )

add_instructions()
