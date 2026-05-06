import streamlit as st
import pandas as pd
import pickle

# Load the trained model
model = pickle.load(open('car_price_model.pkl', 'rb'))

st.title("Car Price Prediction App")
st.write("Enter the car details to predict the selling price.")

# 1. Create input fields for the user
present_price = st.number_input("Present Market Price (in lakhs)", min_value=0.0)
kms_driven = st.number_input("Kilometers Driven", min_value=0)
owner = st.selectbox("Number of Previous Owners", [0, 1, 3])
age = st.number_input("Age of the Car", min_value=0, max_value=50)

# Match the categorical encoding from your notebook
fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
fuel_map = {"Petrol": 0, "Diesel": 1, "CNG": 2}

seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
seller_map = {"Dealer": 0, "Individual": 1}

transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
trans_map = {"Manual": 0, "Automatic": 1}

# 2. Predict button
if st.button("Predict Selling Price"):
    # Arrange inputs in the exact order the model was trained on
    # Check your X.columns in the notebook to confirm this order!
    features = [[
        present_price, 
        kms_driven, 
        owner, 
        age, 
        fuel_map[fuel_type], 
        seller_map[seller_type], 
        trans_map[transmission]
    ]]
    
    prediction = model.predict(features)
    st.success(f"The estimated selling price is ₹{prediction[0]:.2f} Lakhs")