import streamlit as st
import pickle
import numpy as np

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="wide")

# ===== CUSTOM CSS =====
st.markdown("""
<style>
.main { background-color: #f0f2f6; }
h1 { color: #1f4037; text-align: center; font-family: 'Arial'; }
.stButton>button {
    background-color: #1f4037;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODEL =====
# Make sure 'car_price_model.pkl' is uploaded to your GitHub repo
model = pickle.load(open('car_price_model.pkl', 'rb'))

# ===== TITLE =====
st.markdown("<h1>🚗 Car Price Prediction</h1>", unsafe_allow_html=True)
st.write("### Enter car details below 👇")

# ===== INPUT LAYOUT =====
col1, col2 = st.columns(2)

with col1:
    present_price = st.number_input("💰 Present Price (Lakhs)", 0.5, 100.0, 5.0)
    kms_driven = st.number_input("📍 Kms Driven", 0, 500000, 15000)
    owner = st.selectbox("👤 Previous Owners", [0, 1, 3])

with col2:
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller = st.selectbox("🏢 Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("⚙ Transmission", ["Manual", "Automatic"])
    age = st.number_input("📅 Car Age (Years)", 0, 30, 5)

# ===== ENCODING (Matches Notebook Cell 32) =====
# Fuel_Type: Petrol=0, Diesel=1, CNG=2
fuel_val = 0 if fuel == "Petrol" else (1 if fuel == "Diesel" else 2)
# Seller_Type: Dealer=0, Individual=1
seller_val = 1 if seller == "Individual" else 0
# Transmission: Manual=0, Automatic=1
trans_val = 0 if transmission == "Manual" else 1

# ===== PREDICTION =====
st.markdown("---")
col_btn, col_result = st.columns([1,1])

with col_btn:
    predict_btn = st.button("🚀 Predict")

with col_result:
    if predict_btn:
        # ORDER MUST BE: [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Age]
        features = np.array([[present_price, kms_driven, fuel_val, seller_val, trans_val, owner, age]])

        prediction = model.predict(features)

        if prediction[0] < 0:
            st.error("Invalid Prediction (Price cannot be negative)")
        else:
            st.markdown(f"""
                <div style="color: #555;">Estimated Price</div>
                <div style="font-size: 32px; font-weight: 700; color: #1f4037;">
                    ₹ {round(prediction[0], 2)} Lakh
                </div>
            """, unsafe_allow_html=True)
