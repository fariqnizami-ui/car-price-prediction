# 1. Encoding (Matching your notebook exactly)
# Fuel_Type: Petrol:0, Diesel:1, CNG:2
fuel_val = 0 if fuel == "Petrol" else (1 if fuel == "Diesel" else 2)

# Seller_Type: Dealer:0, Individual:1
seller_val = 1 if seller == "Individual" else 0

# Transmission: Manual:0, Automatic:1
trans_val = 1 if transmission == "Automatic" else 0

# 2. Prediction Button
if st.button("Calculate Market Value"):
    # MUST be 7 features in this exact order:
    features = np.array([[present_price, kms_driven, fuel_val, seller_val, trans_val, owner, age]])
    
    prediction = model.predict(features)
    
    st.success(f"Estimated Price: ₹ {round(prediction[0], 2)} Lakh")import streamlit as st
import pickle
import numpy as np

# ===== PAGE CONFIG =====
st.set_page_config(page_title="CarValue Pro | Dark", page_icon="🏎️", layout="centered")

# ===== DARK MODE PREMIUM CSS =====
st.markdown("""
<style>
    /* Main background to Black */
    .stApp {
        background-color: #000000;
    }
    
    /* Card styling for dark mode */
    .prediction-card {
        background-color: #111827;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #1e293b;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        text-align: center;
    }
    
    /* Text Color Adjustments */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Input field styling */
    .stNumberInput input, .stSelectbox div, .stSlider div {
        color: white !important;
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODEL =====
@st.cache_resource
def load_model():
    return pickle.load(open('car_price_model.pkl', 'rb'))

model = load_model()

# ===== HEADER =====
st.markdown("<h1>🏎️ CarValue Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>AI-powered car valuation in Dark Mode</p>", unsafe_allow_html=True)
st.markdown("---")

# ===== INPUT SECTION =====
with st.container():
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### Vehicle Info")
        present_price = st.slider("Original Showroom Price (Lakhs)", 0.5, 50.0, 7.5, step=0.1)
        age = st.number_input("Vehicle Age (Years)", 0, 25, 4)
        kms_driven = st.number_input("Distance Traveled (Kms)", 0, 300000, 20000, step=500)
        owner = st.selectbox("Previous Owners", [0, 1, 3])

    with col2:
        st.markdown("### Technical Specs")
        fuel = st.selectbox("Fuel Category", ["Petrol", "Diesel", "CNG"])
        seller = st.radio("Sales Channel", ["Dealer", "Individual"], horizontal=True)
        transmission = st.radio("Gearbox Type", ["Manual", "Automatic"], horizontal=True)

# ===== ENCODING LOGIC =====
fuel_val = 0 if fuel == "Petrol" else (1 if fuel == "Diesel" else 2)
seller_val = 1 if seller == "Individual" else 0
trans_val = 0 if transmission == "Manual" else 1

# ===== PREDICTION SECTION =====
st.write("##") 
if st.button("Calculate Market Value"):
    # Feature order: [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Age]
    features = np.array([[present_price, kms_driven, fuel_val, seller_val, trans_val, owner, age]])
    prediction = model.predict(features)[0]
    
    st.markdown("---")
    
    if prediction < 0:
        st.warning("⚠️ The provided data doesn't match a realistic market profile.")
    else:
        st.markdown(f"""
            <div class="prediction-card">
                <h3 style='color: #94a3b8; margin-bottom: 0;'>Estimated Resale Value</h3>
                <h1 style='color: #3b82f6; font-size: 48px; margin-top: 10px;'>₹ {round(prediction, 2)} Lakh</h1>
                <p style='color: #64748b; font-size: 14px;'>Valuation complete.</p>
            </div>
        """, unsafe_allow_html=True)
