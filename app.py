import streamlit as st
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(layout="wide", page_title="Insurance Dashboard")

# Custom CSS for dark theme
st.markdown("""
    <style>
        body {
            background-color: #0b1d3a;
            color: #f5f5f5;
        }
        .stApp {
            background-color: #0b1d3a;
            color: #f5f5f5;
        }
        h1, h2, h3, h4, h5 {
            color: #f5f5f5;
        }
        .css-1v0mbdj p, .css-1v0mbdj {
            color: #f5f5f5;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv("data/insurance.data.aggregated.csv")

# Fix typo if present
if "TotalNumberOfInsurancePoliciesPurchaed" in df.columns:
    df.rename(columns={"TotalNumberOfInsurancePoliciesPurchaed": "TotalPoliciesPurchased"}, inplace=True)

# Sidebar filters
st.sidebar.title("🔎 Filters")
selected_channel = st.sidebar.multiselect("Marketing Channel", df["Marketing Channel"].unique(), default=df["Marketing Channel"].unique())
selected_device = st.sidebar.multiselect("Device Category", df["Device Category"].unique(), default=df["Device Category"].unique())

# Apply filters
filtered_df = df[
    (df["Marketing Channel"].isin(selected_channel)) &
    (df["Device Category"].isin(selected_device))
]

# Title
st.title("📊 Insurance Website Analytics Dashboard")
st.markdown("Explore performance metrics and traffic insights from your insurance website.")

# KPIs
st.markdown("### 💡 Key Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("👥 Total Users", int(filtered_df["Users"].sum()))
kpi2.metric("📝 Total Quotes", int(filtered_df["TotalNumberOfInsuranceQuotes"].sum()))
kpi3.metric("📄 Policies Purchased", int(filtered_df["TotalPoliciesPurchased"].sum()))
kpi4.metric("💰 Total Revenue (£)", f"{filtered_df['Revenue'].sum():,.2f}")

kpi5, kpi6 = st.columns(2)
kpi5.metric("📈 Avg. Session Duration (s)", f"{filtered_df['Avg. Session Duration'].mean():.1f}")
kpi6.metric("📄 Avg. Pages / Session", f"{filtered_df['Pages / Session'].mean():.2f}")

# Charts
st.markdown("### 📌 User Distribution by Marketing Channel")
channel_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Marketing Channel", sort='-y'),
    y="Users",
    color="Marketing Channel"
).properties(width=700, height=400)
st.altair_chart(channel_chart, use_container_width=True)

st.markdown("### 🖥️ Device Category Comparison")
device_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="Device Category",
    y="Users",
    color="Device Category"
).properties(width=700, height=400)
st.altair_chart(device_chart, use_container_width=True)

# Scatterplot
st.markdown("### 🔍 Session Engagement (Scatter Plot)")
session_df = filtered_df[["Pages / Session", "Avg. Session Duration", "Marketing Channel", "Device Category", "Users"]].dropna()
session_chart = alt.Chart(session_df).mark_circle().encode(
    x=alt.X("Pages / Session", title="Pages per Session"),
    y=alt.Y("Avg. Session Duration", title="Avg. Session Duration (s)"),
    color="Marketing Channel",
    size="Users",
    tooltip=["Marketing Channel", "Device Category", "Users", "Pages / Session", "Avg. Session Duration"]
).interactive().properties(height=450)
st.altair_chart(session_chart, use_container_width=True)

# Data preview
st.markdown("### 🔍 Preview of Filtered Data")
st.dataframe(filtered_df)
