import streamlit as st
from auth import register_user

def show_register_page():
    st.title("Register")

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
        with st.form(key='register_form', clear_on_submit=True):
            st.text_input("Username", key="register_username")
            st.text_input("Password", type="password", key="register_password")
            st.text_input("Confirm Password", type="password", key="register_password_confirm")
            register_button = st.form_submit_button("Register")
            
            if register_button:
                username = st.session_state.register_username
                password = st.session_state.register_password
                password_confirm = st.session_state.register_password_confirm
                if password != password_confirm:
                    st.error("Passwords do not match")
                else:
                    success, message = register_user(username, password)
                    if success:
                        st.success(message)
                        st.info("Please go to the login page to log in.")
                    else:
                        st.error(message)

    st.markdown('<div class="centered-form"></div>', unsafe_allow_html=True)
