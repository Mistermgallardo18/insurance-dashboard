# Pie Chart: Users by Marketing Channel
st.header("🥧 Pie Chart: Users by Marketing Channel")
pie_data = filtered_df.groupby("Marketing Channel")["Users"].sum().reset_index()
pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Users", type="quantitative"),
    color=alt.Color(field="Marketing Channel", type="nominal"),
    tooltip=["Marketing Channel", "Users"]
).properties(width=600, height=400)
st.altair_chart(pie_chart, use_container_width=True)

# Scatter Chart: Revenue vs Users by Device
st.header("📉 Scatter Chart: Revenue vs Users")
scatter_chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x=alt.X("Users", title="Total Users"),
    y=alt.Y("Revenue", title="Total Revenue (£)"),
    color=alt.Color("Device Category", title="Device"),
    tooltip=["Marketing Channel", "Device Category", "Users", "Revenue"]
).interactive().properties(width=700, height=400)
st.altair_chart(scatter_chart, use_container_width=True)

# Bubble Chart: Quotes vs Policies (Bubble Size = Revenue)
st.header("🔵 Bubble Chart: Quotes vs Policies Purchased")
bubble_data = filtered_df[[
    "TotalNumberOfInsuranceQuotes",
    "TotalNumberOfInsurancePoliciesPurchaed",
    "Revenue",
    "Marketing Channel"
]].dropna()

if bubble_data.empty:
    st.warning("⚠️ No data available for bubble chart with current filters.")
else:
    bubble_chart = alt.Chart(bubble_data).mark_circle().encode(
        x=alt.X("TotalNumberOfInsuranceQuotes", title="Number of Quotes"),
        y=alt.Y("TotalNumberOfInsurancePoliciesPurchaed", title="Policies Purchased"),
        size=alt.Size("Revenue", title="Revenue (£)", scale=alt.Scale(range=[10, 800])),
        color="Marketing Channel",
        tooltip=["Marketing Channel", "Revenue", "TotalNumberOfInsuranceQuotes", "TotalNumberOfInsurancePoliciesPurchaed"]
    ).interactive().properties(width=700, height=400)
    st.altair_chart(bubble_chart, use_container_width=True)
