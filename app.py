import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Load data
df = pd.read_csv("data/insurance.data.aggregated.csv")

# Title
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

# Pie Chart (Plotly)
st.header("🥧 Pie Chart: Users by Marketing Channel")
pie_data = filtered_df.groupby("Marketing Channel")["Users"].sum().reset_index()
fig_pie = px.pie(
    pie_data,
    names="Marketing Channel",
    values="Users",
    title="User Share by Marketing Channel",
    hole=0.4
)
st.plotly_chart(fig_pie, use_container_width=True)

# Bar Chart (Altair)
st.header("📈 Users by Marketing Channel")
channel_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Marketing Channel:N", sort='-y'),
    y="Users:Q",
    color="Marketing Channel:N"
).properties(width=700)
st.altair_chart(channel_chart, use_container_width=True)

# Bar Chart: Device Category
st.header("📱 Users by Device Category")
device_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="Device Category:N",
    y="Users:Q",
    color="Device Category:N"
)
st.altair_chart(device_chart, use_container_width=True)

# New Session Engagement Overview (Bar Plot using Plotly)
st.header("📊 Session Engagement Overview")
session_df = filtered_df[[
    "Marketing Channel", "Pages / Session", "Avg. Session Duration"
]].dropna()

if session_df.empty:
    st.warning("⚠️ No data available for current filter selection.")
else:
    session_bar = px.bar(
        session_df,
        x="Marketing Channel",
        y="Avg. Session Duration",
        color="Pages / Session",
        barmode="group",
        title="Average Session Duration by Marketing Channel",
        labels={"Avg. Session Duration": "Duration (s)", "Pages / Session": "Pages"},
        height=400
    )
    st.plotly_chart(session_bar, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📊 Dashboard created by **Michael Gallardo** | Powered by Streamlit + Altair + Plotly")
