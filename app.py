import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time

# Set up Streamlit page
st.set_page_config(page_title="Dashboard", page_icon="🌲", layout="wide")
st.subheader("🛹 Insurance Descriptive Analytics")
st.markdown("##")

# Show the sidebar
# st.sidebar.image("data/logo.png", caption="Online Analytics")  # Commented out to prevent FileNotFoundError

# Load data from CSV in the 'data/' folder
@st.cache_data
def load_data():
    return pd.read_csv("data/insurance.data.aggregated.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Please filter")
region = st.sidebar.multiselect(
    "Please select region",
    options=df["Region"].dropna().unique(),
    default=df["Region"].dropna().unique()
)
location = st.sidebar.multiselect(
    "Please select location",
    options=df["Location"].dropna().unique(),
    default=df["Location"].dropna().unique()
)
construction = st.sidebar.multiselect(
    "Please select construction",
    options=df["Construction"].dropna().unique(),
    default=df["Construction"].dropna().unique()
)

df_selection = df.query(
    "Region==@region & Location==@location & Construction==@construction"
)

# HOME page function
def Home():
    with st.expander("Tabular View"):
        showData = st.multiselect("Select columns to view:", df_selection.columns, default=[])
        st.dataframe(df_selection[showData] if showData else df_selection)

    # Metrics
    total_investment = float(df_selection['Investment'].sum())
    investment_mode = float(df_selection['Investment'].mode()[0]) if not df_selection['Investment'].mode().empty else 0
    investment_mean = float(df_selection['Investment'].mean())
    investment_median = float(df_selection['Investment'].median())
    total_rating = float(df_selection['Rating'].sum())

    tab1, tab2, tab3, tab4, tab5 = st.columns(5, gap="medium")
    with tab1:
        st.info("Total Investment", icon="📌")
        st.metric(label="Sum (KES)", value=f"{total_investment:,.0f}")
    with tab2:
        st.info("Most Frequent Investment", icon="📌")
        st.metric(label="Mode (KES)", value=f"{investment_mode:,.0f}")
    with tab3:
        st.info("Average Investment", icon="📌")
        st.metric(label="Mean (KES)", value=f"{investment_mean:,.0f}")
    with tab4:
        st.info("Central Investment", icon="📌")
        st.metric(label="Median (KES)", value=f"{investment_median:,.0f}")
    with tab5:
        st.info("Total Rating", icon="📌")
        st.metric(label="Rating", value=numerize(total_rating), help=f"Total Rating: {total_rating}")

    st.markdown("---")

# GRAPHS page function
def graphs():
    investment_by_business_type = (
        df_selection.groupby(by="BusinessType").count()[['Investment']].sort_values(by="Investment")
    )
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="💼 Investment by Business Type",
        color_discrete_sequence=["#0077b6"] * len(investment_by_business_type),
        template="plotly_dark"
    )

    investment_by_state = df_selection.groupby(by="State").count()[['Investment']]
    fig_state = px.line(
        investment_by_state,
        x=investment_by_state.index,
        y='Investment',
        title="📍 Investment by State",
        color_discrete_sequence=["#00b4d8"],
        template="plotly_dark"
    )

    left, right = st.columns(2)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

# PROGRESS page function
def Progressbar():
    st.markdown(
        """<style>.stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #99ff99, #FFFF00)
        }</style>""", unsafe_allow_html=True)
    target = 2_500_000_000
    current = df_selection["Investment"].sum()
    percent = round((current / target) * 100)
    mybar = st.progress(0)

    if percent >= 100:
        st.subheader("🎯 Target achieved!")
    else:
        st.write(f"You have attained {percent}% of your KES {target:,.2f} target.")
        for percent_complete in range(percent):
            time.sleep(0.005)
            mybar.progress(percent_complete + 1, text="Target Progress")

# Sidebar menu
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "graph-up"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        st.subheader(f"📊 {selected} Dashboard")
        Home()
        graphs()
    elif selected == "Progress":
        st.subheader(f"📈 {selected} Tracking")
        Progressbar()
        graphs()

sideBar()

# Hide Streamlit branding (optional)
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
