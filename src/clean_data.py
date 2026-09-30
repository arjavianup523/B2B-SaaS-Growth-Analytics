import pandas as pd

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR



def load_data():

    customers_df = pd.read_csv(
        RAW_DATA_DIR / "customers.csv"
    )

    subscriptions_df = pd.read_csv(
        RAW_DATA_DIR / "subscriptions.csv"
    )

    transactions_df = pd.read_csv(
        RAW_DATA_DIR / "transactions.csv"
    )

    usage_df = pd.read_csv(
        RAW_DATA_DIR / "product_usage.csv"
    )

    return (
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    )



def clean_customers(customers_df):

    print("\nCleaning Customers Data...")

    # Standardize text columns
    customers_df["industry"] = (
        customers_df["industry"]
        .str.strip()
        .str.title()
    )

    customers_df["country"] = (
        customers_df["country"]
        .str.strip()
        .str.upper()
    )

    customers_df["acquisition_channel"] = (
        customers_df["acquisition_channel"]
        .str.strip()
    )

    # Fill missing values
    customers_df["industry"] = (
        customers_df["industry"]
        .fillna("Unknown")
    )

    customers_df["country"] = (
        customers_df["country"]
        .fillna("Unknown")
    )

    # Convert signup date
    customers_df["signup_date"] = pd.to_datetime(
        customers_df["signup_date"],
        errors="coerce"
    )

    return customers_df



def clean_subscriptions(subscriptions_df):

    print("\nCleaning Subscriptions Data...")

    # Standardize text
    subscriptions_df["plan"] = (
        subscriptions_df["plan"]
        .str.strip()
        .str.title()
    )

    subscriptions_df["status"] = (
        subscriptions_df["status"]
        .str.strip()
        .str.title()
    )

    # Convert dates
    subscriptions_df["start_date"] = pd.to_datetime(
        subscriptions_df["start_date"],
        errors="coerce"
    )

    subscriptions_df["end_date"] = pd.to_datetime(
        subscriptions_df["end_date"],
        errors="coerce"
    )

    # Convert price to numeric
    subscriptions_df["monthly_price"] = pd.to_numeric(
        subscriptions_df["monthly_price"],
        errors="coerce"
    )

    return subscriptions_df



def clean_transactions(transactions_df):

    print("\nCleaning Transactions Data...")

    # Remove duplicate transactions
    before = len(transactions_df)

    transactions_df = transactions_df.drop_duplicates(
        subset=["transaction_id"]
    )

    after = len(transactions_df)

    print(
        f"Removed {before - after} duplicate transaction(s)."
    )

    # Standardize transaction type
    transactions_df["transaction_type"] = (
        transactions_df["transaction_type"]
        .str.strip()
        .str.lower()
    )

    # Convert dates
    transactions_df["transaction_date"] = pd.to_datetime(
        transactions_df["transaction_date"],
        errors="coerce"
    )

    # Convert amount to numeric
    transactions_df["amount"] = pd.to_numeric(
        transactions_df["amount"],
        errors="coerce"
    )

    return transactions_df



def clean_product_usage(usage_df):

    print("\nCleaning Product Usage Data...")

    
    usage_df["usage_month"] = pd.to_datetime(
        usage_df["usage_month"],
        errors="coerce"
    )

    
    usage_df["active_users"] = pd.to_numeric(
        usage_df["active_users"],
        errors="coerce"
    )

    usage_df["sessions"] = pd.to_numeric(
        usage_df["sessions"],
        errors="coerce"
    )

    usage_df["features_used"] = pd.to_numeric(
        usage_df["features_used"],
        errors="coerce"
    )

    return usage_df



def validate_data(
    customers_df,
    subscriptions_df,
    transactions_df,
    usage_df
):

    print("\n" + "=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)

    print("\nCustomers:")
    print(customers_df.isnull().sum())

    print("\nSubscriptions:")
    print(subscriptions_df.isnull().sum())

    print("\nTransactions:")
    print(transactions_df.isnull().sum())

    print("\nProduct Usage:")
    print(usage_df.isnull().sum())

    print("\nRow counts:")

    print(
        f"Customers:     {len(customers_df):,}"
    )

    print(
        f"Subscriptions: {len(subscriptions_df):,}"
    )

    print(
        f"Transactions:  {len(transactions_df):,}"
    )

    print(
        f"Product Usage: {len(usage_df):,}"
    )



def save_processed_data(
    customers_df,
    subscriptions_df,
    transactions_df,
    usage_df
):

    customers_df.to_csv(
        PROCESSED_DATA_DIR / "customers_clean.csv",
        index=False
    )

    subscriptions_df.to_csv(
        PROCESSED_DATA_DIR / "subscriptions_clean.csv",
        index=False
    )

    transactions_df.to_csv(
        PROCESSED_DATA_DIR / "transactions_clean.csv",
        index=False
    )

    usage_df.to_csv(
        PROCESSED_DATA_DIR / "product_usage_clean.csv",
        index=False
    )

    print("\nProcessed files saved successfully.")




def main():

    print("=" * 60)
    print("B2B SaaS GROWTH ANALYTICS - DATA CLEANING")
    print("=" * 60)

    # Load
    (
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    ) = load_data()

    # Clean
    customers_df = clean_customers(
        customers_df
    )

    subscriptions_df = clean_subscriptions(
        subscriptions_df
    )

    transactions_df = clean_transactions(
        transactions_df
    )

    usage_df = clean_product_usage(
        usage_df
    )

    # Validate
    validate_data(
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    )

    # Save
    save_processed_data(
        customers_df,
        subscriptions_df,
        transactions_df,
        usage_df
    )

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()