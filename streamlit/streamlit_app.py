
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="E-Commerce Analytics", layout="wide")

session = get_active_session()

st.title("🛒 E-Commerce Sales Analytics")
st.caption("Snowflake • dbt • Apache Airflow • Streamlit")

@st.cache_data(ttl=300)
def load_data():
    query = """
        SELECT
            ORDER_ID,
            CUSTOMER_ID,
            ORDER_DATE,
            TOTAL_AMOUNT
        FROM ECOMMERCE_DB.MARTS.FCT_ORDERS
    """
    return session.sql(query).to_pandas()

df = load_data()
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"])

st.sidebar.header("Filters")

min_date = df["ORDER_DATE"].min().date()
max_date = df["ORDER_DATE"].max().date()

date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[
        (df["ORDER_DATE"].dt.date >= start_date)
        & (df["ORDER_DATE"].dt.date <= end_date)
    ]

total_orders = len(df)
total_revenue = df["TOTAL_AMOUNT"].sum()
total_customers = df["CUSTOMER_ID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Unique Customers", f"{total_customers:,}")

st.divider()

st.subheader("Monthly Revenue")

monthly = (
    df.assign(MONTH=df["ORDER_DATE"].dt.to_period("M").dt.to_timestamp())
    .groupby("MONTH", as_index=False)["TOTAL_AMOUNT"]
    .sum()
    .set_index("MONTH")
)

st.bar_chart(monthly)

st.subheader("Monthly Order Volume")

orders_monthly = (
    df.assign(MONTH=df["ORDER_DATE"].dt.to_period("M").dt.to_timestamp())
    .groupby("MONTH")
    .size()
    .rename("ORDERS")
)

st.line_chart(orders_monthly)

st.subheader("Recent Orders")

st.dataframe(
    df.sort_values("ORDER_DATE", ascending=False).head(20),
    use_container_width=True,
    hide_index=True
)
