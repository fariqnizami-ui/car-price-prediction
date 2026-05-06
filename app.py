import streamlit as st
import pickle
import numpy as np

# ===== PAGE CONFIG =====
st.set_page_config(page_title="CarValue Pro", page_icon="🏎️", layout="centered")

# ===== PREMIUM CUSTOM CSS =====
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f4f7f6;
    }
    /* Prediction card styling */
    .prediction-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
    }
    /* Heading styling */
    h1 {
        color: #1e293b;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
    }
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODEL =====
# Using st.cache_resource so the model doesn't reload every time you click a button
@st.cache_resource
def load_model():
    return pickle.load(open('car_price_model.pkl', 'rb'))

model = load_model()

# ===== HEADER =====
st.markdown("<h1>🏎️ CarValue Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Instant AI-powered car valuation based on market trends</p>", unsafe_allow_html=True)
st.markdown("---")

# ===== INPUT SECTION =====
with st.container():
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("Vehicle Info")
        present_price = st.slider("Original Showroom Price (Lakhs)", 0.5, 50.0, 7.5, step=0.1)
        age = st.number_input("Vehicle Age (Years)", 0, 25, 4)
        kms_driven = st.number_input("Distance Traveled (Kms)", 0, 300000, 20000, step=500)
        owner = st.segmented_control("Previous Owners", [0, 1, 3], default=0)

    with col2:
        st.subheader("Technical Specs")
        fuel = st.selectbox("Fuel Category", ["Petrol", "Diesel", "CNG"])
        seller = st.radio("Sales Channel", ["Dealer", "Individual"], horizontal=True)
        transmission = st.radio("Gearbox Type", ["Manual", "Automatic"], horizontal=True)

# ===== ENCODING LOGIC (Matches Notebook Cell 32) =====
fuel_val = 0 if fuel == "Petrol" else (1 if fuel == "Diesel" else 2)
seller_val = 1 if seller == "Individual" else 0
trans_val = 0 if transmission == "Manual" else 1

# ===== PREDICTION SECTION =====
st.write("##") # Add spacing
if st.button("Calculate Market Value"):
    # Features order from your training: [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Age]
    features = np.array([[present_price, kms_driven, fuel_val, seller_val, trans_val, owner, age]])
    prediction = model.predict(features)[0]
    
    st.markdown("---")
    
    # Custom Prediction Result Display
    if prediction < 0:
        st.warning("⚠️ The provided data doesn't match a realistic market profile.")
    else:
        st.markdown(f"""
            <div class="prediction-card">
                <h3 style='color: #64748b; margin-bottom: 0;'>Estimated Resale Value</h3>
                <h1 style='color: #2563eb; font-size: 48px; margin-top: 10px;'>₹ {round(prediction, 2)} Lakh</h1>
                <p style='color: #94a3b8; font-size: 14px;'>Price based on current market demand and vehicle condition.</p>
            </div>
        """, unsafe_allow_html=True)
