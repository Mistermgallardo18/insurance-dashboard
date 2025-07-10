import pandas as pd
import altair as alt
import plotly.express as px
import streamlit as st

# Load data
df = pd.read_csv("data/insurance.data.aggregated.csv")

# Page config
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

# KPIs
st.header("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Users", int(filtered_df["Users"].sum()))
col2.metric("📄 Total Quotes", int(filtered_df["TotalNumberOfInsuranceQuotes"].sum()))
col3.metric("✅ Policies Purchased", int(filtered_df["TotalNumberOfInsurancePoliciesPurchaed"].sum()))

col4, col5 = st.columns(2)
col4.metric("💰 Revenue (£)", f"{filtered_df['Revenue'].sum():,.2f}")
col5.metric("⏱️ Avg. Session Duration (s)", f"{filtered_df['Avg. Session Duration'].mean():.1f}")

# Row 1 - Marketing Channel: Bar + Pie
st.markdown("## 📊 Channel Overview")
left_col, right_col = st.columns(2)
with left_col:
    st.subheader("📈 Users by Marketing Channel")
    channel_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("Marketing Channel:N", sort='-y'),
        y="Users:Q",
        color="Marketing Channel:N"
    ).properties(width=350)
    st.altair_chart(channel_chart, use_container_width=True)
with right_col:
    st.subheader("🥧 User Share by Channel")
    pie_data = filtered_df.groupby("Marketing Channel")["Users"].sum().reset_index()
    pie_fig = px.pie(pie_data, names="Marketing Channel", values="Users")
    st.plotly_chart(pie_fig, use_container_width=True)

# Row 2 - Device Category & Session Engagement
st.markdown("## 📱 Device & Engagement")
col3, col4 = st.columns(2)
with col3:
    st.subheader("📱 Users by Device")
    device_chart = alt.Chart(filtered_df).mark_bar().encode(
        x="Device Category:N",
        y="Users:Q",
        color="Device Category:N"
    )
    st.altair_chart(device_chart, use_container_width=True)
with col4:
    st.subheader("📉 Session Engagement by Channel")
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
