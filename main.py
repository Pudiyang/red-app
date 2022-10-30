import time

import extra_streamlit_components as stx
import streamlit as st
from PIL import Image
from deploy import predict_hd
def check_password():
    """Returns `True` if the user had a correct password."""
    def check_password():
        st.session_state["password_correct"] = True

    if "password_correct" not in st.session_state:
        st.radio("Log in as:", ['Doctor', 'Patient'], key="user_type")
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Log in", on_click=check_password)
    else:
        return st.session_state["password_correct"]

if check_password():
    def routing_zero():
        def handle_patient_profile() -> None:
            if not st.session_state.first_name:
                st.error("First Name is required!", icon="🚨")
                return
            if not st.session_state.gender:
                st.error("Gender is required!", icon="🚨")
                return
            st.success(st.session_state.first_name + "'s profile created successfully!", icon="✅")
            # st.session_state.step = 1

        with st.form(key='PP'):
            st.text_input('First Name', key='first_name')
            st.text_input('Last Name', key='last_name')
            st.selectbox('Gender', ['M', 'F'], key='gender')
            st.text_input('Phone Number', key='phone_number')
            st.text_input('Email', key='email')
            st.date_input('Date of Birth', key='birthday')
            st.form_submit_button('Save and Continue', on_click=handle_patient_profile)


    def routing_one():
        def handle_get_prediction() -> None:
            # interact with AI module
            # st.session_state.step = 2
            predict_hd(st.session_state.age, st.session_state.gender, st.session_state.cpt\
                       , st.session_state.rbp, st.session_state.cho,  st.session_state.fbs\
                       , st.session_state.ecg, st.session_state.mhr, st.session_state.ea\
                       , st.session_state.op, st.session_state.ss)



        with st.form(key='IF'):
            st.selectbox('Gender', ['M', 'F'], key='gender')
            st.selectbox('ChestPainType:', ['ASY', 'ATA', 'NAP', 'TA'], key='cpt')
            st.selectbox('RestingECG:', ['LVH', 'Normal', 'ST'], key='ecg')
            st.selectbox('ExerciseAngina:', ['N', 'Y'], key='ea')
            st.selectbox('ST_Slope:', ['Down', 'Flat', 'Up'], key='ss')
            st.number_input('Age:', min_value=0, max_value=100, value=1, key='age')
            st.number_input('RestingBP:', min_value=0, max_value=1000, value=1, key='rbp')
            st.number_input('Cholesterol:', min_value=0, max_value=1000, value=1, key='cho')
            st.number_input('FastingBS:', min_value=0, max_value=100, value=1, key='fbs')
            st.number_input('MaxHR:', min_value=0, max_value=1000, value=1, key='mhr')
            st.number_input('Oldpeak:', min_value=0, max_value=100, value=1, key='op')
            st.form_submit_button('Get Prediction', on_click=handle_get_prediction)


    def routing_two():
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1)
        st.markdown("# Here is your report!")


    with st.sidebar:
        # Header
        image = Image.open('logo.png')
        st.image(image, width=260)
        'This is a prototype user interface for the RED project.'

    # Step bar
    if 'step' not in st.session_state:
        st.session_state.step = 0
    step = stx.stepper_bar(steps=['Patient Profile', 'Input Features', 'Get Prediction'])
    # Routing
    if step == 0:
        routing_zero()
    elif step == 1:
        routing_one()
    elif step == 2:
        routing_two()
