import pandas as pd
import joblib

# Load the model
clf_model = joblib.load("rfc_model.pkl")


# prepare the input data according to the processing of training data


def predict_hd(Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS,
               RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope):
    if Sex == 'F':
        Sex = '0'
    else:
        Sex = '1'

    if ChestPainType == 'ASY':
        ChestPainType = 0
    elif ChestPainType == 'ATA':
        ChestPainType = 1
    elif ChestPainType == 'NAP':
        ChestPainType = 2
    elif ChestPainType == 'TA':
        ChestPainType = 3

    if RestingECG == 'LVH':
        RestingECG = 0
    elif RestingECG == 'Normal':
        RestingECG = 1
    elif RestingECG == 'ST':
        RestingECG = 2

    if ExerciseAngina == 'N':
        ExerciseAngina = 0
    elif ExerciseAngina == 'Y':
        ExerciseAngina = 1

    if ST_Slope == 'Down':
        ST_Slope = 0
    elif ST_Slope == 'Flat':
        ST_Slope = 1
    elif ST_Slope == 'Up':
        ST_Slope = 2

    # Perform the prediction
    predict_output = clf_model.predict(
        pd.DataFrame([[Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG,
                       MaxHR, ExerciseAngina, Oldpeak, ST_Slope]],
                     columns=['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG',
                              'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']))
    print(predict_output.tolist())
    return predict_output




# st.title('Head Disease Prediction')
#
# st.header('Enter the mandatory categorical fields')
#
# Sex = st.selectbox('Sex:', ['F', 'M'])
# ChestPainType = st.selectbox('ChestPainType:', ['ASY', 'ATA', 'NAP', 'TA'])
# RestingECG = st.selectbox('RestingECG:', ['LVH', 'Normal', 'ST'])
# ExerciseAngina = st.selectbox('ExerciseAngina:', ['N', 'Y'])
# ST_Slope = st.selectbox('ST_Slope:', ['Down', 'Flat', 'Up'])
#
# st.header('Enter the mandatory readings fields')
# Age = st.number_input('Age:', min_value=0, max_value=100, value=1)
# RestingBP = st.number_input('RestingBP:', min_value=0, max_value=1000, value=1)
# Cholesterol = st.number_input('Cholesterol:', min_value=0, max_value=1000, value=1)
# FastingBS = st.number_input('FastingBS:', min_value=0, max_value=100, value=1)
# MaxHR = st.number_input('MaxHR:', min_value=0, max_value=1000, value=1)
# Oldpeak = st.number_input('Oldpeak:', min_value=0, max_value=100, value=1)
#
#
# if st.button('Predict Heart Disease'):
#     hd = predict_hd(Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG,
#                        MaxHR, ExerciseAngina, Oldpeak, ST_Slope)
#     print(hd)
#     st.success(f'Your prediction is {hd[0]}')


