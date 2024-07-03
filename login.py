import streamlit as st
from auth import login_user

def show_login_page():
    st.title("Login")

    st.markdown(
        """
        <style>
        .centered-form {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 70vh;
        }
        .centered-form form {
            width: 300px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        with st.form(key='login_form', clear_on_submit=True):
            st.text_input("Username", key="login_username")
            st.text_input("Password", type="password", key="login_password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                username = st.session_state.login_username
                password = st.session_state.login_password
                success, user_or_message = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.error(user_or_message)

    st.markdown('<div class="centered-form"></div>', unsafe_allow_html=True)
