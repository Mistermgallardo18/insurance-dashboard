import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time

# Page config
st.set_page_config(page_title="Dashboard", page_icon="🌲", layout="wide")
st.subheader("🛹 Insurance Descriptive Analytics")
st.markdown("##")

# Sidebar image
st.sidebar.image("data/logo.png", caption="Online Analytics")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/insurance.data.aggregated.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Please filter")
region = st.sidebar.multiselect(
    "Please select region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)
location = st.sidebar.multiselect(
    "Please select location",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)
construction = st.sidebar.multiselect(
    "Please select construction",
    options=df["Construction"].unique(),
    default=df["Construction"].unique()
)

df_selection = df.query(
    "Region==@region & Location==@location & Construction==@construction"
)

# Home page
def Home():
    with st.expander("📋 Filtered Table"):
        showData = st.multiselect("Select columns to view:", df_selection.columns, default=[])
        if showData:
            st.write(df_selection[showData])
        else:
            st.write(df_selection)

    # Key metrics
    total_investment = float(df_selection['Investment'].sum())
    investment_mode = float(df_selection['Investment'].mode()[0])
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
        st.info("Median Investment", icon="📌")
        st.metric(label="Median (KES)", value=f"{investment_median:,.0f}")
    with tab5:
        st.info("Rating", icon="⭐")
        st.metric(label="Total Rating", value=numerize(total_rating), help=f"Exact value: {total_rating}")
    st.markdown("""---""")

# Graphs page
def graphs():
    # Bar chart: Business Type
    investment_by_business_type = (
        df_selection.groupby(by="BusinessType").count()[['Investment']].sort_values(by="Investment")
    )
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="💼 Investment by Business Type",
        color_discrete_sequence=["#0083b8"],
        template="plotly_white"
    )
    fig_investment.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))

    # Line chart: State
    investment_by_state = df_selection.groupby(by="State").count()[['Investment']]
    fig_state = px.line(
        investment_by_state,
        x=investment_by_state.index,
        y="Investment",
        title="📍 Investment by State",
        template="plotly_white"
    )
    fig_state.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickmode="linear"),
        yaxis=dict(showgrid=False)
    )

    left, right = st.columns(2)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

# Progress page
def Progressbar():
    st.markdown(
        """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99, #FFFF00); }</style>""",
        unsafe_allow_html=True
    )
    target = 2500000000
    current = df_selection["Investment"].sum()
    percent = round((current / target) * 100)
    mybar = st.progress(0)

    if percent >= 100:
        st.subheader("🎯 Target Achieved!")
    else:
        st.write(f"You have attained {percent}% of your KES {target:,.2f} target.")
        for i in range(percent):
            time.sleep(0.01)
            mybar.progress(i + 1, text="Investment Target Progress")

# Sidebar routing
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="📊 Main Menu",
            options=["Home", "Progress"],
            icons=["house", "bar-chart"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        st.subheader(f"📌 Page: {selected}")
        Home()
        graphs()
    if selected == "Progress":
        st.subheader(f"📌 Page: {selected}")
        Progressbar()
        graphs()

sideBar()

# Optional: Hide footer and header
st.markdown(
    """
    <style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)
