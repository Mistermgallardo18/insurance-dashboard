import streamlit as st
import pandas as pd
import plotly.express as px
from numerize.numerize import numerize

# Page config
st.set_page_config(page_title="Insurance Dashboard", page_icon="📊", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/insurance.data.aggregated.csv")
    return df

df = load_data()

# Header
st.markdown("<h1 style='text-align: center; color: #fff;'>🏢 Insurance Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("###")

# Sidebar
with st.sidebar:
    st.image("data/logo.png", width=150)
    st.markdown("### Please filter", unsafe_allow_html=True)

    region = st.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
    location = st.multiselect("Select Location", df["Location"].unique(), default=df["Location"].unique())
    construction = st.multiselect("Select Construction", df["Construction"].unique(), default=df["Construction"].unique())

# Filtered Data
filtered_df = df.query("Region == @region & Location == @location & Construction == @construction")

# KPIs
total_investment = filtered_df['Investment'].sum()
most_freq_investment = filtered_df['Investment'].mode()[0]
avg_investment = filtered_df['Investment'].mean()
median_investment = filtered_df['Investment'].median()
total_rating = filtered_df['Rating'].sum()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("📌 Total investment", f"{total_investment:,.0f} KES")
kpi2.metric("📌 Most frequent investment", f"{most_freq_investment:,.0f} KES")
kpi3.metric("📌 Average investment", f"{avg_investment:,.0f} KES")
kpi4.metric("📌 Central investment", f"{median_investment:,.0f} KES")
kpi5.metric("📌 Rating", numerize(total_rating))

st.markdown("---")

# Graphs
left, right = st.columns(2)

# Line chart - Investment by State
investment_by_state = filtered_df.groupby("State")[["Investment"]].sum().reset_index()
line_chart = px.line(investment_by_state, x="State", y="Investment", markers=True, title="📈 Investment by State")
line_chart.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
left.plotly_chart(line_chart, use_container_width=True)

# Bar chart - Investment by Business Type
business_chart = (
    filtered_df.groupby("BusinessType")[["Investment"]].sum().sort_values("Investment", ascending=False).reset_index()
)
bar_chart = px.bar(business_chart, x="Investment", y="BusinessType", orientation='h', title="🏢 Investment by Business Type")
bar_chart.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
right.plotly_chart(bar_chart, use_container_width=True)

# Data Table (optional)
with st.expander("📋 Show raw data"):
    st.dataframe(filtered_df)
