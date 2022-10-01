import json
import pandas as pd
import joblib
import streamlit as st
import requests

# load pipeline
pipe = joblib.load(open("model/preprocess_pipeline.pkl", "rb"))
st.title("Aplikasi Prediksi Telco Customer")
gender = st.selectbox("Gender", ['Male','Female'])
seniorcitizen = st.selectbox("Senior Citizen",['Yes','No'])
partner = st.selectbox("Partner",['Yes','No'])
dependents = st.selectbox("Dependents",['Yes','No'])
tenure = st.number_input("Tenure")
phoneservice = st.selectbox("Phone service",['Yes','No'])
multiplelines = st.selectbox("Multiple lines",['Yes','No'])
internetservice = st.selectbox("Internet service",['Fiber optic', 'DSL', 'No'])
onlinesecurity = st.selectbox("Online security",['Yes','No'])
onlinebackup = st.selectbox("Online backup",['Yes','No'])
deviceprotection = st.selectbox("Device protection",['Yes','No'])
techsupport = st.selectbox("Tech support",['Yes','No'])
streamingtv = st.selectbox("Streaming tv",['Yes','No'])
streamingmovies = st.selectbox("Streaming movies",['Yes','No'])
contract = st.selectbox("Contract",['One year', 'Month-to-month', 'Two year'])
paperlessbilling = st.selectbox("Paperless billing",['Yes','No'])
paymentmethod = st.selectbox("Payment method",['Credit card (automatic)', 'Electronic check', 'Mailed check',
       'Bank transfer (automatic)'])
monthlycharges = st.number_input("Monthly charges")
totalcharges = st.number_input("totalcharges")

new_data = {'gender': gender,
         'seniorcitizen': seniorcitizen,
         'partner' : partner,
         'dependents' :dependents,
         'tenure' : tenure,
         'phoneservice' : phoneservice,
         'multiplelines': multiplelines,
         'internetservice': internetservice,
         'onlinesecurity': onlinesecurity,
         'onlinebackup': onlinebackup,
         'deviceprotection': deviceprotection,
         'techsupport': techsupport,
         'streamingtv': streamingtv,
         'streamingmovies': streamingmovies,
         'contract': contract,
         'paperlessbilling': paperlessbilling,
         'paymentmethod': paymentmethod,
         'monthlycharges': monthlycharges,
         'totalcharges': totalcharges}
new_data = pd.DataFrame([new_data])

# build feature
new_data = pipe.transform(new_data)
new_data = new_data.tolist()

# inference
URL = "http://backend-tf-serving-ikhbar1.herokuapp.com/v1/models/churn_model:predict"
param = json.dumps({
        "signature_name":"serving_default",
        "instances":new_data
    })
r = requests.post(URL, data=param)
if r.status_code == 200:
    res = r.json()
    if res['predictions'][0][0] > 0.5:
        st.title("Customer akan berhenti: Yes")
    else:
        st.title("Customer akan berhenti: No")
else:
    st.title("Unexpected Error")
 