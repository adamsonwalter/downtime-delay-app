import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set page config with custom theme
st.set_page_config(
    page_title="Downtime Impact Simulator",
    page_icon="📈",
    layout="wide"
)

# Custom CSS to make it look polished
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    footer {visibility: hidden;}
    .reportview-container .main footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Set random seed
np.random.seed(42)

# Sidebar - Simulation Settings
st.sidebar.header("🔧 Configure Simulation")
N = st.sidebar.slider("Number of Observations", 100, 5000, 1000, step=100)
downtime_prob = st.sidebar.slider("Downtime Probability", 0.0, 1.0, 0.10, step=0.01)
base_delay_prob = st.sidebar.slider("Base Delay Probability (No Downtime)", 0.0, 1.0, 0.05, step=0.01)
increased_delay_prob = st.sidebar.slider("Delay Probability (With Downtime)", 0.0, 1.0, 0.30, step=0.01)

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

# ---- Main Layout ----
col1, col2 = st.columns([2,1])

with col1:
    st.title("📊 Downtime Impact on Delivery Performance")
    st.write("""
    Analyze how unexpected downtimes at manufacturing nodes influence delivery delays at distribution centers.
    Adjust parameters in the sidebar and explore the outcomes interactively.
    """)

with col2:
    st.image("https://images.unsplash.com/photo-1581091870622-1b71e5d76a91", use_column_width=True)

st.markdown("---")

# Charts Section
st.subheader("📈 Visualize Conditional Delivery Delays")
ct = pd.crosstab(data['Downtime_PlantA'], data['DeliveryDelay_RegionB'], normalize='index')
st.bar_chart(ct)

# Correlation Metric
correlation = np.corrcoef(data['Downtime_PlantA'], data['DeliveryDelay_RegionB'])[0,1]
st.metric(label="Correlation between Downtime and Delivery Delay", value=f"{correlation:.3f}")

# Show Raw Data Option
with st.expander("Show Raw Data"):
    st.dataframe(data)

# Download Button
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Simulation Data",
    data=csv,
    file_name='downtime_delay_simulation.csv',
    mime='text/csv'
)

# Footer Branding
st.markdown("""
---
#### Developed by **BayesGen | Strategic Risk & Optimization AI** 🚀  
##### Walter Adamson is an AI Strategic Analysis and Workflow Specialist helping mid-market industrial companies globally translate complex systems into clear, actionable strategies through visual, generative models.
""")
