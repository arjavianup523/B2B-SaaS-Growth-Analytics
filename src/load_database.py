import pandas as pd
from sqlalchemy import create_engine, text

from src.config import (
    PROCESSED_DATA_DIR,
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
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


def load_processed_data():

    customers_df = pd.read_csv(
        PROCESSED_DATA_DIR / "customers_clean.csv"
    )

    subscriptions_df = pd.read_csv(
        PROCESSED_DATA_DIR / "subscriptions_clean.csv"
    )

    transactions_df = pd.read_csv(
        PROCESSED_DATA_DIR / "transactions_clean.csv"
    )

    usage_df = pd.read_csv(
        PROCESSED_DATA_DIR / "product_usage_clean.csv"
    )

    return (
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    )


def prepare_data(
    customers_df,
    subscriptions_df,
    transactions_df,
    usage_df
):

    customers_df["signup_date"] = pd.to_datetime(
        customers_df["signup_date"]
    )

    subscriptions_df["start_date"] = pd.to_datetime(
        subscriptions_df["start_date"]
    )

    subscriptions_df["end_date"] = pd.to_datetime(
        subscriptions_df["end_date"]
    )

    transactions_df["transaction_date"] = pd.to_datetime(
        transactions_df["transaction_date"]
    )

    usage_df["usage_month"] = pd.to_datetime(
        usage_df["usage_month"]
    )

    return (
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    )


def main():

    print("=" * 60)
    print("B2B SaaS GROWTH ANALYTICS - DATABASE LOADING")
    print("=" * 60)

    engine = create_database_engine()

    print("\nDatabase connection created.")

    (
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    ) = load_processed_data()

    (
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    ) = prepare_data(
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    )

    print("\nLoading customers...")
    customers_df.to_sql(
        "customers",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Customers loaded: {len(customers_df):,}")

    print("\nLoading subscriptions...")
    subscriptions_df.to_sql(
        "subscriptions",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Subscriptions loaded: {len(subscriptions_df):,}")

    print("\nLoading transactions...")
    transactions_df.to_sql(
        "transactions",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Transactions loaded: {len(transactions_df):,}")

    print("\nLoading product usage...")
    usage_df.to_sql(
        "product_usage",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Product Usage loaded: {len(usage_df):,}")

    print("\n" + "=" * 60)
    print("DATABASE VERIFICATION")
    print("=" * 60)

    tables = [
        "customers",
        "subscriptions",
        "transactions",
        "product_usage"
    ]

    with engine.connect() as connection:

        for table in tables:

            result = connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            )

            count = result.scalar()

            print(f"{table:<20} {count:,} rows")

    print("\n" + "=" * 60)
    print("DATABASE LOADING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()