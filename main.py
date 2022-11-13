import time

import extra_streamlit_components as stx
import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import Image
from deploy import predict_hd

def check_password():
    def check_password():
        st.session_state["password_correct"] = True

    if "password_correct" not in st.session_state:
        st.markdown("# Log in")
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Log in", on_click=check_password)
    else:
        return st.session_state["password_correct"]


if check_password():
    def go_to_create_profile():
        st.session_state.step = 0
    def go_to_input_features():
        st.session_state.step = 1
    def go_to_prediction():
        st.session_state.step = 2
    def go_to_email_sending():
        st.session_state.step = 3

    def routing_zero():
        def handle_patient_profile() -> None:
            if not st.session_state.first_name:
                st.error("First Name is required!", icon="🚨")
                return
            if not st.session_state.gender:
                st.error("Gender is required!", icon="🚨")
                return
            if not st.session_state.email:
                st.error("Email is required!", icon="🚨")
                return
            st.session_state['patient_id'] = st.session_state.email
            st.success(st.session_state.first_name + "'s profile created successfully!", icon="✅")
            go_to_input_features()

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
            result, accuracy, fig = predict_hd(st.session_state.age, st.session_state.gender, st.session_state.cpt
                                               , st.session_state.rbp, st.session_state.cho, st.session_state.fbs
                                               , st.session_state.ecg, st.session_state.mhr, st.session_state.ea
                                               , st.session_state.op, st.session_state.ss)
            if result == 1:
                st.session_state['result'] = 'YES'
            else:
                st.session_state['result'] = 'NO'
            st.session_state['accuracy'] = accuracy * 100
            st.session_state['fig'] = fig
            go_to_prediction()


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

        st.markdown("### Prediction Report")
        st1, st2 = st.columns(2)
        st.metric(label="Email", value=st.session_state.patient_id)
        with st1:
            st.metric(label="Prediction Result", value=st.session_state.result, help='Yes: has HF, No: Does not have HF')
        with st2:
            st.metric(label="Accuracy", value=str(st.session_state.accuracy) + "%")

        st.button('Approve', on_click=go_to_email_sending)
        st.button('Reject')

        st.markdown('--- ---')
        st.markdown('#### Factors affecting the prediction in decreasing order')
        st.pyplot(fig=st.session_state.fig)
        st.markdown('#### For more information check below')
        st.markdown("- **Age**: age of the patient [years]")
        st.markdown("- **Sex**: gender of the patient [M: Male, F: Female]")
        st.markdown(
            "- ChestPainType: chest pain type [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]")
        st.markdown("- **RestingBP**: resting blood pressure [mm Hg]")
        st.markdown("- **Cholesterol**: serum cholesterol [mm/dl]")
        st.markdown("- **FastingBS**: fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: otherwise]")
        st.markdown(
            "- **RestingECG**: resting electrocardiogram results [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions "
            "and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular "
            "hypertrophy by Estes' criteria]")
        st.markdown("- **MaxHR**: maximum heart rate achieved [Numeric value between 60 and 202]")
        st.markdown("- **ExerciseAngina**: exercise-induced angina [Y: Yes, N: No]")
        st.markdown("- **Oldpeak**: oldpeak = ST [Numeric value measured in depression]")
        st.markdown("- **ST_Slope**: the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]")

    def routing_three():
        #def () -> None:
            st.markdown("### Sending Report")
            if 'count' not in st.session_state:
                st.session_state.count = 0

            msg_from = '1215139249@qq.com'
            passwd = 'wcedtcjsqjzabaeb'
            with st.form("Sending email"):
                receiver = st.text_input("Receiver",str(st.session_state.patient_id))
                to = [receiver]

                # 设置邮件内容
                msg = MIMEMultipart()
                content = st.text_area("Feedback to the patient",'Dear Patient, \nYour heart health report has been successfully generated. Please find an attached report with the email. \nThank you!')
                msg.attach(MIMEText(content, 'plain', 'utf-8'))

                # attachment open
                image_data1 = open('test1.png', 'rb')
                msg.attach(MIMEImage(image_data1.read()))
                image_data1.close()
                image_data2 = open('test2.png', 'rb')
                msg.attach(MIMEImage(image_data2.read()))
                image_data2.close()

                # 设置邮件主题
                theme = st.text_input("Subject",'Check out your heart health prediction report!')

                msg['Subject'] = theme

                msg['From'] = msg_from


                # 开始发送
                submitted = st.form_submit_button("Send")
                if submitted:
                    st.session_state.count += 1
                    if st.session_state.count > 1:
                        st.warning("Don't send too many email！")
                    else:
                        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                        s.login(msg_from, passwd)
                        s.sendmail(msg_from, to, msg.as_string())
                        st.success("Done！")


    with st.sidebar:
        # Header
        image = Image.open('logo.png')
        st.image(image, width=260)
        'This is a prototype user interface for the RED project.'

    if 'step' not in st.session_state:
        st.markdown("# Welcome to Red")
        st.markdown("### Patient Profiles")
        st.button("Create New Patient Profile", on_click=go_to_create_profile)
        df = pd.read_csv('Patients.csv')
        st.table(df)

        patient_id = st.selectbox('Choose Patient', [i[2] for i in df.values.tolist()])
        st.session_state['patient_id'] = patient_id
        st.button("Input Features for Chosen Patient", on_click=go_to_input_features)
    else:
        # Step bar
        step_str = stx.tab_bar(data=[
            stx.TabBarItemData(id=0, title="Profile", description="Create Patient Profile"),
            stx.TabBarItemData(id=1, title="Features", description="Input Clinical Features"),
            stx.TabBarItemData(id=2, title="Prediction", description="Get prediction from AI model "),
            stx.TabBarItemData(id=3, title="Sharing", description="Share email autonomously")
        ], default=st.session_state.step)
        step = int(step_str)

        # Routing
        if step == 0:
            routing_zero()
        elif step == 1:
            routing_one()
        elif step == 2:
            routing_two()
        elif step == 3:
            routing_three()