import streamlit as st
import pandas as pd
import altair as alt

# ─── Load Data ─────────────────────────────────────────────────────────────
df = pd.read_csv("data/insurance.data.aggregated.csv")

# If your CSV has the typo, rename it in code:
if "TotalNumberOfInsurancePoliciesPurchaed" in df.columns:
    df.rename(
        columns={"TotalNumberOfInsurancePoliciesPurchaed": "TotalNumberOfInsurancePoliciesPurchased"},
        inplace=True
    )

# ─── App Title ──────────────────────────────────────────────────────────────
st.title("📊 Insurance Website Analytics Dashboard")
st.markdown("An interactive Streamlit dashboard to explore your insurance website data.")

# ─── Sidebar Filters ────────────────────────────────────────────────────────
st.sidebar.header("🔎 Filter the Data")
channels = df["Marketing Channel"].unique()
devices  = df["Device Category"].unique()

selected_channel = st.sidebar.multiselect("Marketing Channel", channels, default=list(channels))
selected_device  = st.sidebar.multiselect("Device Category", devices, default=list(devices))

# ─── Filtered Data ──────────────────────────────────────────────────────────
filtered_df = df[
    df["Marketing Channel"].isin(selected_channel) &
    df["Device Category"].isin(selected_device)
]

# ─── Key Metrics ───────────────────────────────────────────────────────────
st.header("📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Users", int(filtered_df["Users"].sum()))
col2.metric("🧾 Total Quotes", int(filtered_df["TotalNumberOfInsuranceQuotes"].sum()))
col3.metric("✅ Policies Purchased", int(filtered_df["TotalNumberOfInsurancePoliciesPurchased"].sum()))

col4, col5 = st.columns(2)
col4.metric("💰 Total Revenue (£)", f"{filtered_df['Revenue'].sum():,.2f}")
col5.metric("⏱️ Avg. Session Duration (s)", f"{filtered_df['Avg. Session Duration'].mean():.1f}")

st.markdown("---")

# ─── Chart 1: User Distribution ────────────────────────────────────────────
st.subheader("📣 User Distribution by Marketing Channel")
channel_chart = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x=alt.X("Marketing Channel", sort="-y"),
        y="Users",
        color="Marketing Channel"
    )
    .properties(width=700, height=300)
)
st.altair_chart(channel_chart, use_container_width=True)

# ─── Chart 2: Device Comparison ────────────────────────────────────────────
st.subheader("📱 Device Type Comparison")
device_chart = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x="Device Category",
        y="Users",
        color="Device Category"
    )
    .properties(width=700, height=300)
)
st.altair_chart(device_chart, use_container_width=True)

# ─── Chart 3: Revenue by Channel ───────────────────────────────────────────
st.subheader("💸 Revenue by Marketing Channel")
revenue_chart = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x=alt.X("Marketing Channel", sort="-y"),
        y="Revenue",
        color="Marketing Channel",
        tooltip=["Marketing Channel", "Revenue"]
    )
    .properties(width=700, height=300)
)
st.altair_chart(revenue_chart, use_container_width=True)

# ─── Chart 4: Session Engagement ───────────────────────────────────────────
st.subheader("🔍 Session Engagement Overview")
session_df = filtered_df[[
    "Pages / Session",
    "Avg. Session Duration",
    "Marketing Channel",
    "Device Category",
    "Users"
]].dropna()

if session_df.empty:
    st.warning("⚠️ No session data available for these filter settings.")
else:
    session_chart = (
        alt.Chart(session_df)
        .mark_circle()
        .encode(
            x=alt.X("Pages / Session", title="Pages per Session"),
            y=alt.Y("Avg. Session Duration", title="Avg. Session Duration (s)"),
            color=alt.Color("Marketing Channel", title="Marketing Channel"),
            size=alt.Size("Users", title="Users", scale=alt.Scale(range=[20, 400])),
            tooltip=[
                "Marketing Channel",
                "Device Category",
                "Users",
                "Pages / Session",
                "Avg. Session Duration"
            ]
        )
        .interactive()
        .properties(width=700, height=400)
    )
    st.altair_chart(session_chart, use_container_width=True)

# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("📊 Dashboard by Michael Gallardo | Built with Streamlit, Altair & Pandas")
