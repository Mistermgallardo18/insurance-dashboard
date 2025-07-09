import streamlit as st
import pandas as pd
import altair as alt

# Load data
df = pd.read_csv("data/insurance.data.aggregated.csv")

# Title
st.title("Insurance Website Analytics Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_channel = st.sidebar.multiselect("Marketing Channel", df["Marketing Channel"].unique(), default=df["Marketing Channel"].unique())
selected_device = st.sidebar.multiselect("Device Category", df["Device Category"].unique(), default=df["Device Category"].unique())

# Filter data
filtered_df = df[
    (df["Marketing Channel"].isin(selected_channel)) &
    (df["Device Category"].isin(selected_device))
]

# Display KPIs
st.header("Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Users", int(filtered_df["Users"].sum()))
col2.metric("Total Quotes", int(filtered_df["TotalNumberOfInsuranceQuotes"].sum()))
col3.metric("Total Policies Purchased", int(filtered_df["TotalNumberOfInsurancePoliciesPurchaed"].sum()))

col4, col5 = st.columns(2)
col4.metric("Total Revenue (£)", f"{filtered_df['Revenue'].sum():,.2f}")
col5.metric("Avg. Session Duration (s)", f"{filtered_df['Avg. Session Duration'].mean():.1f}")

# Charts
st.header("User Distribution by Marketing Channel")
channel_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Marketing Channel", sort='-y'),
    y="Users",
    color="Marketing Channel"
).properties(width=700)
st.altair_chart(channel_chart, use_container_width=True)

st.header("Device Type Comparison")
device_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="Device Category",
    y="Users",
    color="Device Category"
)
st.altair_chart(device_chart, use_container_width=True)

st.header("Session Stats")
session_chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x="Pages / Session",
    y="Avg. Session Duration",
    color="Marketing Channel",
    tooltip=["Marketing Channel", "Device Category", "Users"]
).interactive()
st.altair_chart(session_chart, use_container_width=True)
