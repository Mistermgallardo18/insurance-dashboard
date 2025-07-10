import streamlit as st
import pandas as pd
import altair as alt

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
col3.metric("✅ Total Policies Purchased", int(filtered_df["TotalNumberOfInsurancePoliciesPurchaed"].sum()))

col4, col5 = st.columns(2)
col4.metric("💰 Total Revenue (£)", f"{filtered_df['Revenue'].sum():,.2f}")
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

# Session Chart Preview
st.subheader("📋 Data preview for session chart")
st.write(filtered_df[["Pages / Session", "Avg. Session Duration", "Marketing Channel"]].dropna())

st.write("🧮 Column types:")
st.write(filtered_df[["Pages / Session", "Avg. Session Duration"]].dtypes)

# Scatter Plot: Session Engagement Overview
st.header("🔍 Session Engagement Overview")

# Prepare data
session_df = filtered_df[[
    "Pages / Session",
    "Avg. Session Duration",
    "Marketing Channel",
    "Device Category",
    "Users"
]].copy().dropna()

if session_df.empty:
    st.warning("⚠️ No data available for the current filter selection.")
else:
    session_chart = alt.Chart(session_df).mark_circle(size=60).encode(
        x=alt.X("Pages / Session", title="Pages per Session"),
        y=alt.Y("Avg. Session Duration", title="Avg. Session Duration (s)"),
        color=alt.Color("Marketing Channel", title="Marketing Channel"),
        size=alt.Size("Users", title="Users", scale=alt.Scale(range=[10, 500])),
        tooltip=["Marketing Channel", "Device Category", "Users", "Pages / Session", "Avg. Session Duration"]
    ).interactive().properties(width=700, height=400)

    st.altair_chart(session_chart, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📊 Dashboard created by **Michael Gallardo** | Powered by Streamlit + Altair + Pandas")
