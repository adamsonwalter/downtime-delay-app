import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page config
st.set_page_config(page_title="Downtime vs Delivery Delay Analysis", layout="wide")

# Set random seed for reproducibility
np.random.seed(42)

# Sidebar inputs
st.sidebar.header("Simulation Settings")
N = st.sidebar.slider("Number of Observations", 100, 5000, 1000, step=100)
downtime_prob = st.sidebar.slider("Downtime Probability", 0.0, 1.0, 0.10, step=0.01)
base_delay_prob = st.sidebar.slider("Base Delay Probability (No Downtime)", 0.0, 1.0, 0.05, step=0.01)
increased_delay_prob = st.sidebar.slider("Increased Delay Probability (With Downtime)", 0.0, 1.0, 0.30, step=0.01)

# Generate synthetic data
downtime = np.random.binomial(1, downtime_prob, N)
delivery_delay = np.zeros(N)
for i in range(N):
    if downtime[i] == 1:
        delivery_delay[i] = np.random.binomial(1, increased_delay_prob)
    else:
        delivery_delay[i] = np.random.binomial(1, base_delay_prob)

# Create DataFrame
data = pd.DataFrame({
    'Downtime_PlantA': downtime,
    'DeliveryDelay_RegionB': delivery_delay
})

# Main App
st.title("📊 Downtime Impact on Delivery Delay")
st.markdown("Use this tool to explore the relationship between unexpected downtimes at Plant A and delivery delays in Region B.")

# Show data
if st.checkbox("Show Raw Data"):
    st.dataframe(data)

# Visualization
st.subheader("Conditional Probability Visualization")
ct = pd.crosstab(data['Downtime_PlantA'], data['DeliveryDelay_RegionB'], normalize='index')
st.bar_chart(ct)

# Quick correlation
correlation = np.corrcoef(data['Downtime_PlantA'], data['DeliveryDelay_RegionB'])[0,1]
st.metric(label="Quick Pearson Correlation", value=f"{correlation:.3f}")

# Download synthetic dataset
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Synthetic Data as CSV",
    data=csv,
    file_name='synthetic_downtime_delivery.csv',
    mime='text/csv',
)

# Footer
st.markdown("---")
st.markdown("App developed by BayesGen | Strategic Risk & Optimization AI")
