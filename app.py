# 1. Create the binary (0/1) features based on user selection
# Fuel Type Logic
fuel_diesel = 1 if fuel_type == "Diesel" else 0
fuel_petrol = 1 if fuel_type == "Petrol" else 0

# Seller Type Logic
seller_individual = 1 if seller_type == "Individual" else 0

# Transmission Logic
transmission_manual = 1 if transmission == "Manual" else 0

# 2. Arrange features in the EXACT order of X.columns from your notebook
# Based on your notebook, the order is likely:
# [Present_Price, Kms_Driven, Owner, Age, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]

if st.button("Predict Selling Price"):
    features = [[
        present_price, 
        kms_driven, 
        owner, 
        age, 
        fuel_diesel, 
        fuel_petrol, 
        seller_individual, 
        transmission_manual
    ]]
    
    prediction = model.predict(features)
    st.success(f"The estimated selling price is ₹{prediction[0]:.2f} Lakhs")
