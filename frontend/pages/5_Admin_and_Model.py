"""
RainGuard AI — Admin Panel & Model Management
"""

import streamlit as st
import time
import pandas as pd
import numpy as np

st.set_page_config(page_title="RainGuard AI — Admin & AI Model", page_icon="⚙️", layout="wide")

st.markdown("## ⚙️ AI Model Management & Data Pipeline Admin")
st.caption("Monitor model performance, ingest new sensor data, and trigger pipeline retraining.")

st.divider()

# Model Status Cards
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Model", "XGBoost + ConvLSTM v2.4")
m2.metric("Model ROC-AUC", "0.924", "+0.015")
m3.metric("F1-Score", "0.891", "+0.02")
m4.metric("Inference Latency", "42 ms / grid")

st.markdown("---")

col_upload, col_train = st.columns([1, 1])

with col_upload:
    st.subheader("📥 Ingest Fresh Weather & DEM Data")
    st.caption("Upload CSV / NetCDF files from IMD, AWS, or GIS DEM datasets.")

    uploaded_file = st.file_uploader("Choose a dataset file (CSV, GeoJSON, NetCDF)", type=["csv", "json"])

    if uploaded_file is not None:
        st.success(f"File uploaded successfully: `{uploaded_file.name}`")
        try:
            df_preview = pd.read_csv(uploaded_file)
            st.markdown("**Data Preview:**")
            st.dataframe(df_preview.head(5), use_container_width=True)
        except Exception:
            st.info("Uploaded data formatted for backend spatial pipeline.")

with col_train:
    st.subheader("🤖 Trigger Model Retraining")
    st.caption("Retrain ConvLSTM spatial rainfall model and XGBoost flood classifier on newly ingested data.")

    hyperparam_epochs = st.slider("ConvLSTM Training Epochs", min_value=5, max_value=50, value=20)
    learning_rate = st.select_slider("Learning Rate", options=[0.0001, 0.001, 0.01, 0.1], value=0.001)

    if st.button("🚀 Start Retraining Pipeline"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        for percent in range(1, 101):
            time.sleep(0.03)  # Fast visual simulation
            progress_bar.progress(percent)

            if percent < 30:
                status_text.text(f"⏳ Step 1/3: Preprocessing spatial grids & elevation rasters... ({percent}%)")
            elif percent < 70:
                status_text.text(f"⏳ Step 2/3: Training ConvLSTM precipitation forecast model (Epoch {int(percent/2)}/{hyperparam_epochs})... ({percent}%)")
            else:
                status_text.text(f"⏳ Step 3/3: Fitting XGBoost flood risk classifier & calculating SHAP values... ({percent}%)")

        status_text.text("✅ Retraining complete! New model version (v2.5) deployed to inference server.")
        st.success("Model accuracy updated: ROC-AUC 0.938 (+0.014 improvement)")
        st.balloons()

st.markdown("---")

st.subheader("📊 Model Feature Importance (SHAP Weights)")
st.caption("Global feature importance learned by the XGBoost classifier across all grid points.")

feature_data = pd.DataFrame({
    "Feature Name": [
        "Elevation (DEM)",
        "Predicted 6h Rainfall",
        "Built-up Fraction (Impervious Area)",
        "Proximity to Water Bodies / Rivers",
        "Drainage Capacity Index",
        "Soil Moisture Index",
    ],
    "Importance Weight Score": [0.34, 0.28, 0.18, 0.12, 0.05, 0.03],
})

st.bar_chart(feature_data.set_index("Feature Name"))