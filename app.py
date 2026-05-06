import streamlit as st
import pickle
import numpy as np

# ===== PAGE CONFIG =====
st.set_page_config(page_title="CarValue AI", page_icon="🏎️", layout="centered")

# ===== LUXURY DARK THEME CSS =====
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    /* Glassmorphism effect for the input area */
    div[data-testid="stVerticalBlock"] > div:has(div.stColumn) {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1 {
        color: #00d4ff;
        text-align: center;
        font-family: 'Trebuchet MS';
        text-shadow: 2px 2px 10px rgba(0, 212, 255, 0.3);
    }
    /* Styling labels */
    label {
        color: #e0e0e0 !important;
        font-weight: bold !important;
    }
    /* Prediction Button */
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        color: white;
        border: none;
        border-radius: 50px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODEL =====
@st.cache_resource
def load_model():
    return pickle.load(open('car_price_model.pkl', 'rb'))

model = load_model()

# ===== HEADER =====
st.markdown("<h1>🏎️ CarValue AI Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Premium vehicle valuation powered by Machine Learning</p>", unsafe_allow_html=True)

# ===== INPUT SECTION =====
col1, col2 = st.columns(2, gap="medium")

with col1:
    present_price = st.number_input("💰 Current Showroom Price (Lakhs)", 0.1, 100.0, 5.0)
    kms_driven = st.number_input("📍 Kilometers Driven", 0, 500000, 15000)
    owner = st.radio("👤 Previous Owners", [0, 1, 3], horizontal=True)

with col2:
    age = st.slider("📅 Age of Vehicle (Years)", 0, 25, 5)
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller = st.selectbox("🏢 Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("⚙️ Transmission", ["Manual", "Automatic"])

# ===== ENCODING (Matches Notebook Cell 32) =====
fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
seller_map = {'Dealer': 0, 'Individual': 1}
trans_map = {'Manual': 0, 'Automatic': 1}

# ===== PREDICTION BUTTON =====
st.write("##")
if st.button("GET INSTANT VALUATION"):
    # Order from Notebook: [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Age]
    features = np.array([[
        present_price, 
        kms_driven, 
        fuel_map[fuel], 
        seller_map[seller], 
        trans_map[transmission], 
        owner, 
        age
    ]])
    
    prediction =
import streamlit as st
import pickle
import numpy as np

# ===== PAGE CONFIG =====
st.set_page_config(page_title="CarValue AI", page_icon="🏎️", layout="centered")

# ===== LUXURY DARK THEME CSS =====
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Trebuchet MS'; }
    label { color: #ffffff !important; font-weight: bold !important; }
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        color: white; border-radius: 50px; height: 3em; width: 100%; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODEL =====
@st.cache_resource
def load_model():
    return pickle.load(open('car_price_model.pkl', 'rb'))

model = load_model()

st.markdown("<h1>🏎️ CarValue AI Predictor</h1>", unsafe_allow_html=True)

# ===== INPUT SECTION =====
col1, col2 = st.columns(2)

with col1:
    present_price = st.number_input("💰 Present Price (Lakhs)", 0.1, 100.0, 5.0)
    kms_driven = st.number_input("📍 Kms Driven", 0, 500000, 15000)
    owner = st.selectbox("👤 Previous Owners", [0, 1, 3])

with col2:
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller = st.selectbox("🏢 Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("⚙️ Transmission", ["Manual", "Automatic"])
    age = st.number_input("📅 Age (Years)", 0, 30, 5)

# ===== ENCODING (Matches Notebook Cell 32) =====
fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
seller_map = {'Dealer': 0, 'Individual': 1}
trans_map = {'Manual': 0, 'Automatic': 1}

# ===== PREDICTION =====
if st.button("GET VALUATION"):
    # Features order: [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Age]
    features = np.array([[
        present_price, 
        kms_driven, 
        fuel_map[fuel], 
        seller_map[seller], 
        trans_map[transmission], 
        owner, 
        age
    ]])
    
    prediction = model.predict(features)[0]
    
    st.markdown("---")
    st.markdown(f"""
        <div style="background: rgba(0, 212, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center;">
            <h3 style="color: #00d4ff;">Estimated Price</h3>
            <h1 style="color: #ffffff;">₹ {round(prediction, 2)} Lakh</h1>
        </div>
    """, unsafe_allow_html=True)
