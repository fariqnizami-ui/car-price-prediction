import streamlit as st
import pandas as pd
import pickle

# 1. Load the model
model = pickle.load(open('car_price_model.pkl', 'rb'))

# 2. Get User Inputs FIRST
st.title("Car Price Prediction")
present_price = st.number_input("Present Price (in lakhs)", 0.0, 50.0, 5.0)
kms_driven = st.number_input("Kms Driven", 0, 500000, 10000)
owner = st.selectbox("Owner", [0, 1, 3])
age = st.number_input("Age of car", 0, 20, 5)

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

# 3. NOW define the variables for the model
fuel_diesel = 1 if fuel_type == "Diesel" else 0
fuel_petrol = 1 if fuel_type == "Petrol" else 0
seller_individual = 1 if seller_type == "Individual" else 0
transmission_manual = 1 if transmission == "Manual" else 0

# 4. Prediction Button
if st.button("Predict"):
    # The order MUST match your X_train columns exactly
    features = [[present_price, kms_driven, owner, age, fuel_diesel, fuel_petrol, seller_individual, transmission_manual]]
    prediction = model.predict(features)
    st.success(f"Predict Price: {prediction[0]:.2f} Lakhs")
cols_to_drop = [c for c in ['Car_Name', 'Year', 'Current_Year'] if c in df.columns]
df.drop(columns=cols_to_drop, inplace=True)
