import streamlit as st
from streamlit_option_menu import option_menu
import requests
import konten as knt
import login as lg
import register as rg
import pandas as pd

# Set the page configuration with a wider layout
st.set_page_config(page_title="Sentiment Analysis App", page_icon=":tada:", layout="wide")

def load_animation(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

animation = load_animation("https://lottie.host/6d2774b5-55cf-408f-abd0-5c47508e00d7/8qRRYQeBRt.json")

konten = knt.Konten('dashboard_name', 'analisis', 'prediksi', 'dataset', animation=animation)

# Function to clear session state and logout user
def logout_user():
    st.session_state.logged_in = False
    st.session_state.pop('username', None)
    st.experimental_rerun()

# Check if the user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = "Home"

if not st.session_state.logged_in:
    menu_option = option_menu(
        menu_title="Authentication",
        options=['Login', 'Register'],
        icons=['box-arrow-in-right', 'pencil-square'],
        menu_icon="cast",
        default_index=0
    )

    if menu_option == 'Login':
        lg.show_login_page()
    elif menu_option == 'Register':
        rg.show_register_page()
else:
    # Add some space to the sidebar
    st.markdown(
        """
        <style>
        .css-1v3fvcr {
            width: 16rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create the sidebar with the option menu and a dropdown
    with st.sidebar:
        selected = option_menu(
            menu_title="Toxic Classification",
            options=['Home', 'Analisis', 'Prediksi', 'Dataset', 'Logout'],
            icons=['house', 'gear-wide-connected', 'file-earmark-bar-graph', 'box-arrow-left'],
            menu_icon="cast",
            default_index=0
        )

        if selected == 'Logout':
            logout_user()

        with st.expander("Preprocessing"):
            category = st.selectbox(
                "Phase 1:",
                ["Phase1","Case Folding", "Tokenizing", "SWR", "Lemmatisasi"]
            )

    # Update the page state based on sidebar selection
    if selected != st.session_state.page:
        st.session_state.page = selected

    if category == "Case Folding":
        st.session_state.page = "Case Folding"
    elif category == "Tokenizing":
        st.session_state.page = "Tokenizing"
    elif category == "SWR":
        st.session_state.page = "SWR"
    elif category == "Lemmatisasi":
        st.session_state.page = "Lemmatisasi"

    # Display the appropriate content based on the current page
    if st.session_state.page == "Home":
        konten.dashboard()
    elif st.session_state.page == "Analisis":
        st.title("Ini adalah halaman analisis")
        konten.show_charts()
    elif st.session_state.page == "Prediksi":
        # st.title("Ini adalah halaman prediksi")
        konten.prdks()
    elif st.session_state.page == "Dataset":
        st.title("Ini adalah halaman dataset")
        st.write(f"Kategori yang dipilih: Dataset")
        path_df = "data/selected_samples.csv"
        konten.dts(path_df)
    elif st.session_state.page == "Case Folding":
        st.title('Ini adalah halaman case folding')
        konten.cs_folding('data/selected_samples.csv')
    elif st.session_state.page == "Tokenizing":
        st.title('Ini adalah halaman tokenizing')
        konten.tknz('data/selected_samples.csv')
    elif st.session_state.page == "SWR":
        st.title('Ini adalah halaman SWR')
        konten.swr('data/selected_samples.csv')
    elif st.session_state.page == "Lemmatisasi":
        st.title('Ini adalah halaman lemmatisasi')
        konten.lemma('data/selected_samples.csv')
