import streamlit as st
import pickle
import numpy as np

# ===== PAGE CONFIG =====
st.set_page_config(page_title="CarValue AI", page_icon="🏎️")

# ===== DARK THEME CSS =====
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1 { color: #00d4ff; text-align: center; }
    label { color: #ffffff !important; font-weight: bold !important; }
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        color: white; border-radius: 50px; width: 100%; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODEL =====
@st.cache_resource
def load_model():
    return pickle.load(open('car_price_model.pkl', 'rb'))

model = load_model()

st.markdown("<h1>🏎️ Car Price Prediction</h1>", unsafe_allow_html=True)

# ===== INPUTS =====
col1, col2 = st.columns(2)
with col1:
    present_price = st.number_input("Present Price (Lakhs)", 0.1, 100.0, 5.0)
    kms_driven = st.number_input("Kms Driven", 0, 500000, 10000)
    owner = st.selectbox("Owners", [0, 1, 3])
    age = st.number_input("Age (Years)", 0, 30, 5)

with col2:
    fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "CNG"])
    seller = st.selectbox("Seller", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

# ===== ENCODING (Matches Notebook Cell 32) =====
fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
seller_map = {'Dealer': 0, 'Individual': 1}
trans_map = {'Manual': 0, 'Automatic': 1}

if st.button("GET VALUATION"):
    # Based on your notebook, the model expects these 8 columns in order:
    # 1. Present_Price, 2. Kms_Driven, 3. Fuel_Type, 4. Seller_Type, 
    # 5. Transmission, 6. Owner, 7. Current_Year, 8. Age
    
    current_year = 2024 # As defined in your notebook
    
    features = np.array([[
        present_price, 
        kms_driven, 
        fuel_map[fuel], 
        seller_map[seller], 
        trans_map[transmission], 
        owner, 
        current_year, 
        age
    ]])
    
    prediction = model.predict(features)
    
    st.markdown(f"""
        <div style="background: rgba(0, 212, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #00d4ff;">
            <h3 style="color: #00d4ff; margin:0;">Estimated Price</h3>
            <h1 style="color: #ffffff; margin:10px;">₹ {round(prediction[0], 2)} Lakh</h1>
        </div>
    """, unsafe_allow_html=True)
