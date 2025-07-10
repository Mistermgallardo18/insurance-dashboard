import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Load data
df = pd.read_csv("data/insurance.data.aggregated.csv")

# Set page config and style
st.set_page_config(page_title="Insurance Analytics Dashboard", layout="wide")

# Background and text color styling
st.markdown(
    """
    <style>
    body {
        background-color: #0c1e3c;
        color: white;
    }
    .css-18e3th9 {
        background-color: #0c1e3c;
    }
    .css-1d391kg {
        color: white;
    }
    .st-bb {
        color: white;
    }
    .st-cw {
        background-color: #0c1e3c;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
col4.metric("💰 Total Revenue (£)", f"{filtered_df['Revenue'].sum():,.2f}")
col5.metric("⏱️ Avg. Session Duration (s)", f"{filtered_df['Avg. Session Duration'].mean():.1f}")

# Charts: Device & Session Engagement
st.header("📱 Device & Engagement")
col6, col7 = st.columns(2)

with col6:
    st.subheader("📊 Users by Device")
    device_chart = px.bar(
        filtered_df,
        x="Device Category",
        y="Users",
        color="Device Category",
        title="Users by Device Category"
    )
    st.plotly_chart(device_chart, use_container_width=True)

with col7:
    st.subheader("📊 Session Engagement by Channel")
    engagement_data = filtered_df.groupby("Marketing Channel")[["Pages / Session", "Avg. Session Duration"]].mean().reset_index()
    engagement_melted = engagement_data.melt(
        id_vars="Marketing Channel",
        value_vars=["Pages / Session", "Avg. Session Duration"],
        var_name="Metric",
        value_name="Value"
    )
    engagement_chart = px.bar(
        engagement_melted,
        x="Marketing Channel",
        y="Value",
        color="Metric",
        barmode="group",
        title="Avg Pages/Session & Duration by Channel"
    )
    st.plotly_chart(engagement_chart, use_container_width=True)

# Pie Chart: Users by Marketing Channel
st.header("🥧 Users Distribution by Channel")
pie_data = filtered_df.groupby("Marketing Channel")["Users"].sum().reset_index()
pie_chart = px.pie(
    pie_data,
    names="Marketing Channel",
    values="Users",
    title="User Share by Marketing Channel"
)
st.plotly_chart(pie_chart, use_container_width=True)

# Bubble Chart: Users vs Quotes (sized by Revenue)
st.header("🫧 Users vs Quotes (Bubble by Revenue)")
bubble_chart = px.scatter(
    filtered_df,
    x="Users",
    y="TotalNumberOfInsuranceQuotes",
    size="Revenue",
    color="Marketing Channel",
    hover_name="Device Category",
    size_max=60,
    title="Users vs Quotes by Revenue and Channel"
)
st.plotly_chart(bubble_chart, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📊 Dashboard created by **Michael Gallardo** | Powered by Streamlit + Altair + Plotly + Pandas")
