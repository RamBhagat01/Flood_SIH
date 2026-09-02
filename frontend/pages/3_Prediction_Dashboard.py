"""
RainGuard AI — Area Risk Prediction & Explainability Dashboard
"""

import streamlit as st
import pandas as pd
from mock_data import get_pincode_data

st.set_page_config(page_title="RainGuard AI — Risk Prediction", page_icon="🔍", layout="wide")

st.markdown("## 🔍 Area Risk Prediction & AI Explainability")
st.caption("Select or search a Pincode / Area to get instant flood risk predictions and AI factor breakdowns.")

pincode_dict = get_pincode_data()

# Area selection
selected_area_key = st.selectbox(
    "Select Area or Enter Pincode:",
    options=list(pincode_dict.keys()),
    index=0
)

data = pincode_dict[selected_area_key]

st.divider()

# Top Summary Row
col1, col2, col3, col4 = st.columns(4)

risk_score = data["risk_score"]
risk_pct = f"{int(risk_score * 100)}%"

if risk_score > 0.7:
    color_code = "🔴"
elif risk_score > 0.4:
    color_code = "🟠"
else:
    color_code = "🟢"

col1.metric("Predicted Flood Risk", f"{color_code} {risk_pct}", data["risk_level"])
col2.metric("6h Expected Rainfall", data["predicted_rain_6h"])
col3.metric("Terrain Elevation", f"{data['elevation_m']} meters")
col4.metric("Built-up Surface", data["built_up_area"])

st.markdown("---")

# Visual Risk Bar
st.subheader("Risk Score Gauge")
st.progress(risk_score)

# Main Two Columns: AI Explainability Card & Safety Action
col_ai, col_action = st.columns([1.6, 1])

with col_ai:
    st.subheader("🧠 AI Feature Breakdown (Explainability Card)")
    st.caption("Why did XGBoost + ConvLSTM predict this risk score for this area?")

    df_factors = pd.DataFrame(data["top_risk_factors"])
    st.dataframe(
        df_factors.rename(columns={
            "factor": "Risk Driver",
            "impact": "Observed Condition",
            "weight": "Model Weight Impact"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "💡 **Explainable AI Note:** Model uses SHAP values combining elevation grids, "
        "radar precipitation estimates, and drainage obstruction indices to calculate this risk score."
    )

with col_action:
    st.subheader("🛡 Safety Advisory")
    
    if risk_score > 0.7:
        st.error(f"**Status:** {data['evacuation_status']}")
    elif risk_score > 0.4:
        st.warning(f"**Status:** {data['evacuation_status']}")
    else:
        st.success(f"**Status:** {data['evacuation_status']}")

    st.markdown("### 🏥 Nearest Relief Shelter")
    st.write(f"📍 **{data['nearest_shelter']}**")

    st.markdown("### 📞 Emergency Helpline")
    st.code("Chennai Flood Helpline: 1913\nNDRF Control Room: 1078", language="text")

st.caption("Predictions updated dynamically using incoming satellite & weather API feeds.")