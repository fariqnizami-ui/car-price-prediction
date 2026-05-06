import streamlit as st
import pickle
import numpy as np

# 1. Load the trained model
# Ensure 'car_price_model.pkl' is in the same folder on GitHub
model = pickle.load(open('car_price_model.pkl', 'rb'))

st.title("🚗 Car Price Prediction")
st.write("Enter the details below to estimate the selling price of your car.")

# 2. User Inputs
present_price = st.number_input("Present Market Price (in lakhs)", min_value=0.0, value=5.0)
kms_driven = st.number_input("Total Kilometers Driven", min_value=0, value=10000)
owner = st.selectbox("Number of Previous Owners", [0, 1, 3])

# Age calculation: User enters the year, we calculate the age
import datetime
current_year = datetime.datetime.now().year
car_year = st.number_input("Year of Manufacture", min_value=1990, max_value=current_year, value=2015)
age = current_year - car_year

# Categorical Inputs
fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

# 3. Convert Inputs to Model Features
# Based on your notebook encoding:
# Fuel_Type: Petrol=0, Diesel=1, CNG=2
fuel_val = 0 if fuel_type == "Petrol" else (1 if fuel_type == "Diesel" else 2)

# Seller_Type: Dealer=0, Individual=1
seller_val = 1 if seller_type == "Individual" else 0

# Transmission: Manual=0, Automatic=1
trans_val = 1 if transmission == "Automatic" else 0

# 4. Prediction Button
if st.button("Predict Selling Price"):
    # The order MUST match your X_train columns from your notebook exactly:
    # [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Age]
    # NOTE: Double check your notebook order. If you used get_dummies, 
    # use the list logic from my previous message.
    
    features = np.array([[present_price, kms_driven, fuel_val, seller_val, trans_val, owner, age]])
    
    prediction = model.predict(features)
    
    # Display the result
    if prediction[0] < 0:
        st.error("Sorry, this car cannot be sold.")
    else:
        st.success(f"The estimated selling price is ₹{prediction[0]:.2f} Lakhs")
