import time

import extra_streamlit_components as stx
import streamlit as st
from PIL import Image


def routing_zero():
    def handle_patient_profile() -> None:
        if not st.session_state.first_name:
            st.error("First Name is required!", icon="🚨")
            return
        if not st.session_state.gender:
            st.error("Gender is required!", icon="🚨")
            return
        st.success(st.session_state.first_name + "'s profile created successfully!", icon="✅")
        st.session_state.step = 1

    with st.form(key='PP'):
        st.text_input('First Name', key='first_name')
        st.text_input('Last Name', key='last_name')
        st.selectbox('Gender', ['-', 'Male', 'Female', 'Non-binary'], key='gender')
        st.text_input('Phone Number', key='phone_number')
        st.text_input('Email', key='email')
        st.date_input('Date of Birth', key='birthday')
        st.form_submit_button('Save and Continue', on_click=handle_patient_profile)


def routing_one():
    def handle_get_prediction() -> None:
        # interact with AI module
        st.session_state.step = 2

    with st.form(key='IF'):
        st.text_input('Features1', key='f1')
        st.text_input('Features2', key='f2')
        st.text_input('Features3', key='f3')
        st.text_input('Features4', key='f4')
        st.text_input('Features5', key='f5')
        st.text_input('Features6', key='f6')
        st.text_input('Features7', key='f7')
        st.text_input('Features8', key='f8')
        st.text_input('Features9', key='f9')
        st.text_input('Features10', key='f10')
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
step = stx.stepper_bar(steps=['Patient Profile', 'Input Features', 'Get Prediction'], default=st.session_state.step)

# Routing
if step == 0:
    routing_zero()
elif step == 1:
    routing_one()
elif step == 2:
    routing_two()
