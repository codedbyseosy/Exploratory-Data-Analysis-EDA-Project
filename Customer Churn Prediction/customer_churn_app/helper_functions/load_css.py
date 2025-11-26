import streamlit as st


# Function to load and apply CSS styles from an external file
def load_css(file_name):
    """
    Loads CSS from a file and applies it to the Streamlit app

    Args:
        file_name (str):  The name/path of the CSS file to load
    """
    # Open the CSS file and reads its content
    with open(file_name) as f:
        # Apply the CSS styles to the Streamlit app
        st.markdown(f'<style>{f.read()}</style', unsafe_allow_html=True)
