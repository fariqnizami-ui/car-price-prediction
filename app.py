import streamlit as st
import pickle
import numpy as np

# ===== LOAD MODEL =====
# Using st.cache_resource so it's fast
@st.cache_resource
def load_model():
    return pickle.load(open('car_price_model.pkl', 'rb'))

model = load_model()

# ===== UI SETUP =====
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗")

st.markdown("<h1 style='text-align: center;'>🚗 Car Price Prediction</h1>", unsafe_allow_html=True)
st.write("---")

# ===== INPUTS =====
col1, col2 = st.columns(2)

with col1:
    present_price = st.number_input("Present Price (In Lakhs)", 0.1, 100.0, 5.0)
    kms_driven = st.number_input("Kms Driven", 0, 500000, 10000)
    owner = st.selectbox("Number of Owners", [0, 1, 3])
    age = st.number_input("Age of Car (Years)", 0, 30, 5)

with col2:
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

# ===== ENCODING (Matches Notebook Cell 32) =====
fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
seller_map = {'Dealer': 0, 'Individual': 1}
trans_map = {'Manual': 0, 'Automatic': 1}

fuel_val = fuel_map[fuel]
seller_val = seller_map[seller]
trans_val = trans_map[transmission]

# ===== PREDICTION =====
if st.button("Predict Selling Price"):
    # The order MUST be: [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Age]
    features = np.array([[present_price, kms_driven, fuel_val, seller_val, trans_val, owner, age]])
    
    prediction = model.predict(features)
    
    if prediction[0] < 0:
        st.error("Sorry, this car cannot be sold.")
    else:
        st.success(f"Estimated Selling Price: ₹ {round(prediction[0], 2)} Lakh")
