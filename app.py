import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Load data
df = pd.read_csv("data/insurance.data.aggregated.csv")

# Title
st.set_page_config(page_title="Insurance Dashboard", layout="wide")
st.title("💼 Insurance Website Analytics Dashboard")

# Sidebar filters
st.sidebar.header("📌 Filters")
selected_channel = st.sidebar.multiselect(
    "Marketing Channel",
    df["Marketing Channel"].dropna().unique(),
    default=df["Marketing Channel"].dropna().unique()
)
selected_device = st.sidebar.multiselect(
    "Device Category",
    df["Device Category"].dropna().unique(),
    default=df["Device Category"].dropna().unique()
)

# Filter data
filtered_df = df[
    (df["Marketing Channel"].isin(selected_channel)) &
    (df["Device Category"].isin(selected_device))
]

# Display KPIs
st.header("📊 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Users", int(filtered_df["Users"].sum()))
col2.metric("📄 Total Quotes", int(filtered_df["TotalNumberOfInsuranceQuotes"].sum()))
col3.metric("✅ Policies Purchased", int(filtered_df["TotalNumberOfInsurancePoliciesPurchaed"].sum()))

col4, col5 = st.columns(2)
col4.metric("💰 Revenue (£)", f"{filtered_df['Revenue'].sum():,.2f}")
col5.metric("⏱️ Avg. Session Duration (s)", f"{filtered_df['Avg. Session Duration'].mean():.1f}")

# Bar Chart: Users by Marketing Channel
st.header("📈 User Distribution by Marketing Channel")
channel_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Marketing Channel:N", sort='-y'),
    y="Users:Q",
    color="Marketing Channel:N"
).properties(width=700)
st.altair_chart(channel_chart, use_container_width=True)

# Bar Chart: Users by Device
st.header("📱 Device Type Comparison")
device_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="Device Category:N",
    y="Users:Q",
    color="Device Category:N"
)
st.altair_chart(device_chart, use_container_width=True)

# Pie Chart: Users by Marketing Channel
st.header("🥧 Pie Chart: Users by Marketing Channel")
pie_data = filtered_df.groupby("Marketing Channel")["Users"].sum().reset_index()
pie_fig = px.pie(pie_data, names="Marketing Channel", values="Users", title="User Share by Channel")
st.plotly_chart(pie_fig, use_container_width=True)

# Line Chart: Avg. Session Duration and Pages/Session
st.header("📉 Session Engagement by Channel")
line_data = filtered_df.groupby("Marketing Channel")[["Pages / Session", "Avg. Session Duration"]].mean().reset_index()
line_fig = px.line(
    line_data,
    x="Marketing Channel",
    y=["Pages / Session", "Avg. Session Duration"],
    markers=True,
    title="Average Session Metrics by Marketing Channel"
)
st.plotly_chart(line_fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📊 Dashboard created by **Michael Gallardo** | Powered by Streamlit + Altair + Plotly + Pandas")
