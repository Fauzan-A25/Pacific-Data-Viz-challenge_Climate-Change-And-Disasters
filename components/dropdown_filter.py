import streamlit as st

def get_selected_country(lang="Indonesia"):
    texts = {
        "Indonesia": "Pilih Negara:",
        "English": "Select Country:"
    }

    df = st.session_state.processed_data
    countries = df["Country"].unique().tolist()
    selected = st.sidebar.selectbox(texts.get(lang, "Pilih Negara:"), countries)
    return selected
