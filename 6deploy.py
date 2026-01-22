import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Load the model and columns
try:
    model = joblib.load('laptop_price_model.pkl')
    model_columns = joblib.load('model_columns.pkl')
except FileNotFoundError:
    st.error("⚠️ Files not found! Please run your save_model script first.")
    st.stop()

# 2. Dynamic Dropdown Lists

# Get all columns that start with "Brand_", "CPU_", "GPU_"
cpu_options = [col.replace("CPU_", "") for col in model_columns if col.startswith("CPU_")]
gpu_options = [col.replace("GPU_", "") for col in model_columns if col.startswith("GPU_")]
all_brands = ["ACER", "ASUS", "COOLER MASTER", "DELL", "GIGABYTE", "HP", "LENOVO", "MSI", "RAZER"]

# 2. Page Configuration
st.title("💻 Tunisian Laptop Price Predictor")
st.markdown("Enter the specs below to get an estimated market price (TND).")
st.set_page_config(page_title="Tunisian Laptop Pricer", page_icon="💻")

# 3. User Input
col1, col2 = st.columns(2)

with col1:
    # Now the user selects the EXACT CPU (e.g., "Intel Core i5-12450H")
    brand = st.selectbox("Brand", sorted(all_brands))
    cpu = st.selectbox("CPU Model", sorted(cpu_options))
    gpu = st.selectbox("GPU Model", sorted(gpu_options))

with col2:
    ram = st.slider("RAM (GB)", 8, 64, 16, step=8)
    storage = st.selectbox("Storage (GB)", [512, 1024, 2048], index=1)
    garentie = st.radio("Warranty (Years)", [1, 2], horizontal=True)

# 4. Prediction Logic
if st.button("🚀 Predict Price"):
    
    # A. Start with all zeros
    input_data = {col: 0 for col in model_columns}
    
    # B. Fill numeric
    input_data['RAM_GB'] = ram
    input_data['Storage_GB'] = storage
    input_data['Garentie'] = garentie
    
    # C. Exact One-Hot Encoding
    # We reconstruct the exact column name. If it exists, we set ONLY that one to 1.
    
    brand_col = f"Brand_{brand}"
    cpu_col = f"CPU_{cpu}"
    gpu_col = f"GPU_{gpu}"
    
    if brand_col in input_data: input_data[brand_col] = 1
    if cpu_col in input_data: input_data[cpu_col] = 1
    if gpu_col in input_data: input_data[gpu_col] = 1

    # D. Predict
    input_df = pd.DataFrame([input_data])
    
    # Show the "debug" table to prove only ONE CPU is selected
    with st.expander("Debugging: Check inputs"):
        # Show only columns that are set to 1
        active_cols = [k for k,v in input_data.items() if v == 1]
        st.write(f"Active Features: {active_cols}")
    
    try:
        log_pred = model.predict(input_df)
        real_price = np.expm1(log_pred)[0]
        st.success(f"💰 Estimated Price: {real_price:,.2f} TND")
    except Exception as e:
        st.error(f"Error: {e}")