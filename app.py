import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time

# Load CSV data
@st.cache_data
def load_data():
    df = pd.read_csv("insurance.data.aggregated.csv")
    return df

df = load_data()

st.set_page_config(page_title="Insurance Dashboard", page_icon="📊", layout="wide")
st.markdown("## 🪻 Insurance Analytics Dashboard 🌷")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Progress"],
        icons=["house", "bar-chart"],
        menu_icon="cast",
        default_index=0
    )

    st.image("https://cdn-icons-png.flaticon.com/512/992/992700.png", width=150)
    st.markdown("### Filter Data")
    selected_channel = st.multiselect("Marketing Channel", options=df["Marketing Channel"].unique(), default=df["Marketing Channel"].unique())
    selected_device = st.multiselect("Device Category", options=df["Device Category"].unique(), default=df["Device Category"].unique())

# Filtered data
filtered_df = df[(df["Marketing Channel"].isin(selected_channel)) & (df["Device Category"].isin(selected_device))]

# Home Tab
if selected == "Home":
    st.markdown("### 📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", int(filtered_df["Users"].sum()))
    col2.metric("Total Quotes", int(filtered_df["TotalNumberOfInsuranceQuotes"].sum()))
    col3.metric("Policies Purchased", int(filtered_df["TotalNumberOfInsurancePoliciesPurchaed"].sum()))
    col4.metric("Revenue (£)", f"{filtered_df['Revenue'].sum():,.2f}")

    col5, col6 = st.columns(2)
    col5.metric("Avg. Pages/Session", f"{filtered_df['Pages / Session'].mean():.2f}")
    col6.metric("Avg. Session Duration (s)", f"{filtered_df['Avg. Session Duration'].mean():.1f}")

    st.markdown("---")

    # Graphs
    st.markdown("### 📊 Charts")
    left, right = st.columns(2)

    with left:
        st.subheader("Users by Marketing Channel")
        chart = px.bar(filtered_df, x="Marketing Channel", y="Users", color="Marketing Channel")
        st.plotly_chart(chart, use_container_width=True)

    with right:
        st.subheader("Users by Device Category")
        chart2 = px.pie(filtered_df, values="Users", names="Device Category", title="User Distribution")
        st.plotly_chart(chart2, use_container_width=True)

# Progress tab
if selected == "Progress":
    st.markdown("### 🎯 Revenue Progress")
    target = 50000
    achieved = filtered_df["Revenue"].sum()
    percent = round((achieved / target) * 100)
    bar = st.progress(0, text=f"{percent}% of £{target:,} goal")

    for i in range(percent):
        time.sleep(0.01)
        bar.progress(i + 1, text=f"{i+1}% of £{target:,} goal")

    if percent >= 100:
        st.success("🎉 Target Achieved!")
    else:
        st.info(f"You have achieved {percent}% of your £{target:,} goal.")

# Hide footer
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
