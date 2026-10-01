import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

from src.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


st.set_page_config(
    page_title="B2B SaaS Growth Analytics",
    page_icon="📊",
    layout="wide"
)


def create_database_engine():
    connection_url = (
        f"mysql+pymysql://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True
    )


@st.cache_data
def load_data():
    engine = create_database_engine()

    customers = pd.read_sql(
        "SELECT * FROM customers",
        engine
    )

    subscriptions = pd.read_sql(
        "SELECT * FROM subscriptions",
        engine
    )

    transactions = pd.read_sql(
        "SELECT * FROM transactions",
        engine
    )

    product_usage = pd.read_sql(
        "SELECT * FROM product_usage",
        engine
    )

    return (
        customers,
        subscriptions,
        transactions,
        product_usage
    )


def main():

    st.title("📊 B2B SaaS Growth Analytics")

    st.markdown(
        "Automated customer, revenue, subscription and "
        "product usage analytics."
    )

    customers, subscriptions, transactions, product_usage = load_data()

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"]
    )

    subscriptions["start_date"] = pd.to_datetime(
        subscriptions["start_date"]
    )

    subscriptions["end_date"] = pd.to_datetime(
        subscriptions["end_date"]
    )

    product_usage["usage_month"] = pd.to_datetime(
        product_usage["usage_month"]
    )

    total_revenue = transactions["amount"].sum()

    total_customers = customers["customer_id"].nunique()

    active_subscriptions = subscriptions[
        subscriptions["status"] == "Active"
    ].shape[0]

    total_transactions = transactions[
        "transaction_id"
    ].nunique()

    mrr = subscriptions.loc[
        subscriptions["status"] == "Active",
        "monthly_price"
    ].sum()

    arr = mrr * 12

    total_subscriptions = len(subscriptions)

    cancelled_subscriptions = subscriptions[
        subscriptions["status"] == "Cancelled"
    ].shape[0]

    churn_rate = (
        cancelled_subscriptions
        / total_subscriptions
        * 100
    )

    paying_customers = transactions[
        "customer_id"
    ].nunique()

    average_revenue_per_customer = (
        total_revenue / paying_customers
        if paying_customers > 0
        else 0
    )

    cancelled_subscriptions_df = subscriptions[
        subscriptions["status"] == "Cancelled"
    ].copy()

    if len(cancelled_subscriptions_df) > 0:

        cancelled_subscriptions_df["lifetime_days"] = (
            cancelled_subscriptions_df["end_date"]
            - cancelled_subscriptions_df["start_date"]
        ).dt.days

        average_lifetime_months = (
            cancelled_subscriptions_df["lifetime_days"].mean()
            / 30
        )

    else:

        average_lifetime_months = 0

    ltv = (
        average_revenue_per_customer
        * average_lifetime_months
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}"
    )

    col2.metric(
        "MRR",
        f"${mrr:,.2f}"
    )

    col3.metric(
        "ARR",
        f"${arr:,.2f}"
    )

    col4.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Customers",
        f"{total_customers:,}"
    )

    col2.metric(
        "Active Subscriptions",
        f"{active_subscriptions:,}"
    )

    col3.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

    col4.metric(
        "Estimated LTV",
        f"${ltv:,.2f}"
    )

    st.divider()

    st.subheader("Revenue Trend")

    monthly_revenue = (
        transactions.assign(
            month=transactions[
                "transaction_date"
            ].dt.to_period("M").astype(str)
        )
        .groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        monthly_revenue.set_index("month")
    )

    st.subheader("Revenue by Transaction Type")

    revenue_by_type = (
        transactions
        .groupby("transaction_type")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(revenue_by_type)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Revenue by Plan")

        customer_revenue = (
            transactions
            .groupby("customer_id")["amount"]
            .sum()
            .reset_index(
                name="total_revenue"
            )
        )

        revenue_by_plan = (
            subscriptions[
                ["customer_id", "plan"]
            ]
            .merge(
                customer_revenue,
                on="customer_id",
                how="inner"
            )
            .groupby("plan")["total_revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(revenue_by_plan)

    with col2:

        st.subheader("Customers by Industry")

        customers_by_industry = (
            customers
            .groupby("industry")["customer_id"]
            .nunique()
            .sort_values(ascending=False)
        )

        st.bar_chart(customers_by_industry)

    st.divider()

    st.subheader("Subscription Performance")

    subscription_summary = (
        subscriptions
        .groupby("plan")
        .agg(
            total_subscriptions=(
                "subscription_id",
                "count"
            ),
            active_subscriptions=(
                "status",
                lambda x: (x == "Active").sum()
            ),
            cancelled_subscriptions=(
                "status",
                lambda x: (x == "Cancelled").sum()
            ),
            average_monthly_price=(
                "monthly_price",
                "mean"
            )
        )
        .reset_index()
    )

    subscription_summary[
        "churn_rate_percent"
    ] = (
        subscription_summary[
            "cancelled_subscriptions"
        ]
        / subscription_summary[
            "total_subscriptions"
        ]
        * 100
    )

    subscription_summary[
        "average_monthly_price"
    ] = subscription_summary[
        "average_monthly_price"
    ].round(2)

    subscription_summary[
        "churn_rate_percent"
    ] = subscription_summary[
        "churn_rate_percent"
    ].round(2)

    st.dataframe(
        subscription_summary,
        width="stretch"
    )

    st.divider()

    st.subheader("Product Usage")

    usage_summary = (
        product_usage
        .groupby("usage_month")
        .agg(
            active_users=(
                "active_users",
                "sum"
            ),
            sessions=(
                "sessions",
                "sum"
            ),
            features_used=(
                "features_used",
                "sum"
            )
        )
        .reset_index()
    )

    usage_summary["usage_month"] = (
        usage_summary["usage_month"]
        .dt.strftime("%Y-%m")
    )

    st.line_chart(
        usage_summary.set_index("usage_month")
    )

    st.divider()

    st.subheader("Top Customers by Revenue")

    top_customers = (
        customers
        .merge(
            transactions,
            on="customer_id",
            how="inner"
        )
        .groupby(
            [
                "customer_id",
                "company_name",
                "industry",
                "country"
            ],
            as_index=False
        )["amount"]
        .sum()
        .rename(
            columns={
                "amount": "total_revenue"
            }
        )
        .sort_values(
            "total_revenue",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        top_customers,
        width="stretch"
    )

    st.divider()

    st.subheader("Business Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.metric(
            "Average Revenue / Paying Customer",
            f"${average_revenue_per_customer:,.2f}"
        )

    with summary_col2:

        st.metric(
            "Average Customer Lifetime",
            f"{average_lifetime_months:.1f} months"
        )


if __name__ == "__main__":
    main()