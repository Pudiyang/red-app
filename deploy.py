import pandas as pd
import joblib
import matplotlib.pyplot as plt



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

    test_df = pd.DataFrame([[Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG,
                   MaxHR, ExerciseAngina, Oldpeak, ST_Slope]],
                 columns=['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG',
                          'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope'])
    predict_output = clf_model.predict(test_df).tolist()
    probability = clf_model.predict_proba(test_df).tolist()
    fe = clf_model.feature_importances_.argsort()

    fig, ax = plt.subplots()
    ax.barh(test_df.columns[fe], clf_model.feature_importances_[fe])
    ax.set_xlabel("Feature Importance")
    ax.set_title('Feature Importance chart')

    return predict_output[0], round(probability[0][1], 4), fig


