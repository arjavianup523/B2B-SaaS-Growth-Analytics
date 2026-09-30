# import random 
# import pandas as pd

# from datetime import datetime,timedelta
# from src.config import RAW_DATA_DIR


# NUM_CUSTOMERS = 1000

# START_DATE =datetime(2025,1,1)
# END_DATE = datetime(2025,12,31)

# INDUSTRIES = [
#     "SaaS",
#     "FinTech",
#     "HealthCare",
#     "E-Commerce",
#     "Education",
#     "Manufacturing",
# ]

# COUNTRIES = [
#     "USA",
#     "UK",
#     "India",
#     "Germany",
#     "Canada",
#     "Australia",
# ]

# ACQUISITION_CHANNELS = [
#     "Organic Search",
#     "Paid Ads",
#     "Referral",
#     "LinkedIn",
#     "Email",
# ]

# PLANS = {
#     "Starter": 99,
#     "Growth": 299,
#     "Business": 799,
#     "Enterprise": 1999,
# }

# TRASACTION_TYPES = [
#     "new",
#     "renewal",
#     "upgrade",
#     "downgrade",
#     "refund",
# ]

# FEATURES = [
#     "Dashboards",
#     "Reports",
#     "Analytics",
#     "Automation",
#     "API",
#     "Integrations",
# ]

# def random_date(start_date,end_date):
#     days_between = (end_date - start_date).days

#     random_days = random.randint(0,days_between)

#     return start_date + timedelta (days=random_days)


# def generate_customers():
#     print("\nGenerating Customers Data...")

#     customers = []

#     for i in range (1,NUM_CUSTOMERS+1):

#         signup_date = random_date(
#             START_DATE,
#             datetime(2025,10,31)
#         )

#         customer = { 
#             "customer_id": f"CUST{i:04d}",
#             "company_name": f"Company_{i}",
#             "industry": random.choice(INDUSTRIES),
#             "country": random.choice(COUNTRIES),
#             "signup_date": signup_date.strftime("%Y-%m-%d"),
#             "acquisition_channel": random.choice(ACQUISITION_CHANNELS),

#         }

#         customers.append(customer)

#     customers_df = pd.DataFrame(customers)

#     customers_df.loc[5, "country"] = None

#     customers_df.loc[10, "industry"] = None

#     customers_df.loc[20, "country"] = "usa"

#     customers_df.loc[30, "industry"] = "saas"

#     print(customers_df.head())

#     customers_df.to_csv(RAW_DATA_DIR / "customers.csv", index=False)
#     return customers_df


# def generate_subscriptions(customers_df):
#     print("\nGenerating Subscription Data...")

#     subscriptions =  []

#     for i, customer in customers_df.iterrows():
#         customer_id = customer["customer_id"]
#         start_date = datetime.strptime(
#             customer["signup_date"],
#             "%Y-%m-%d"
#         )

#         plan = random.choice(list(PLANS.keys()))

#         status = random.choice(
#             [
#                 "Active",
#                 "Active",
#                 "Active",
#                 "Active",
#                 "Canceled",
#             ]

#         )
#         end_date = None
#         if status == "Cancelled":
#             possible_end_date = start_date + timedelta(
#                 days=random.randint(30, 300)
#             )

#             if possible_end_date <= END_DATE:
#                 end_date = possible_end_date.strftime("%Y-%m-%d")
#             else:
#                 status = "Active"

#         subscription = {
#             "subscription_id": f"SUB{i + 1:04d}",
#             "customer_id": customer_id,
#             "plan": plan,
#             "monthly_price": PLANS[plan],
#             "start_date": start_date.strftime("%Y-%m-%d"),
#             "end_date": end_date,
#             "status": status,
#         }

#         subscriptions.append(subscription)
#     subscriptions_df = pd.DataFrame(subscriptions)
#     print(subscriptions_df.head())

#     subscriptions_df.to_csv(
#         RAW_DATA_DIR / "subscriptions.csv",
#         index=False
#     )

#     return subscriptions_df


# def generate_transactions(subscriptions_df):
#     print("\nGenerating Transaction Data...")

#     transactions = []

#     transaction_counter = 1

#     for _, subscription in subscriptions_df.iterrows():
#         start_date = datetime.strptime(
#             subscription["start_date"],
#             "%Y-%m-%d"
#         )

#         end_date = END_DATE

#         if pd.notna(subscription["end_date"]):
#             end_date = datetime.strptime(
#                 subscription["end_date"],
#                 "%Y-%m-%d"
#             )
#         current_date = start_date
#         while current_date <= end_date:
#             transaction_type = "renewal"
#             if current_date == start_date:
#                 transaction_type = "new"
#             else:
#                 random_value = random.random()

#                 if random_value < 0.05:
#                     transaction_type = "upgrade"
#                 elif random_value < 0.10:
#                     transaction_type = "downgrade"
#                 elif random_value < 0.13:
#                     transaction_type = "refund"

#             amount = subscription["monthly_price"]
#             if transaction_type == "upgrade":
#                 amount = round(amount * 1.5, 2)
#             elif transaction_type == "downgrade":
#                 amount = round(amount * 0.5, 2)
#             elif transaction_type == "refund":
#                 amount = -amount

#             transaction = {
#                 "transaction_id": f"TXN{transaction_counter:06d}",
#                 "customer_id": subscription["customer_id"],
#                 "transaction_date": current_date.strftime("%Y-%m-%d"),
#                 "amount": amount,
#                 "transaction_type": transaction_type,
#             }

#             transactions.append(transaction)
#             transaction_counter += 1

#             current_date += timedelta(days=30)

#     transactions_df = pd.DataFrame(transactions)

#     if len(transactions_df) > 10:
#         duplicate_row = transactions_df.iloc[[10]].copy()

#         transactions_df = pd.concat(
#             [
#                 transactions_df,
#                 duplicate_row
#             ],
#             ignore_index=True
#         )
#     print(transactions_df.head())

#     transactions_df.to_csv(
#         RAW_DATA_DIR / "transactions.csv",
#         index=False
#     )
#     return transactions_df

# def generate_product_usage(customers_df):
#     print("\nGenerating Product Usage Data...")

#     usage_data = []

#     months = pd.date_range(
#         start="2025-01-01",
#         end="2025-12-01",
#         freq="MS"
#     )

#     for _, customer in customers_df.iterrows():
#         customer_id = customer["customer_id"]

#         signup_date = datetime.strptime(
#             customer["signup_date"],
#             "%Y-%m-%d"
#         )

#         for month in months:
#             month_date = month.to_pydatetime()

#             if month_date < datetime(
#                 signup_date.year,
#                 signup_date.month,
#                 1
#             ):
#                 continue

#             active_users = random.randint(1, 50)
#             sessions = random.randint(
#                 active_users,
#                 active_users * 20
#             )
#             features_used = random.randint(
#                 1,
#                 len(FEATURES)
#             )
#             usage = {
#                 "customer_id": customer_id,
#                 "usage_month": month.strftime("%Y-%m-%d"),
#                 "active_users": active_users,
#                 "sessions": sessions,
#                 "features_used": features_used,
#             }

#             usage_data.append(usage)

#     usage_df = pd.DataFrame(usage_data)
#     print(usage_df.head())
#     usage_df.to_csv(
#         RAW_DATA_DIR / "product_usage.csv",
#         index=False
#     )
#     return usage_df

# def main():
#     print("=" * 60)
#     print("B2B SaaS GROWTH ANALYTICS - DATA GENERATION")
#     print("=" * 60)

#     customers_df = generate_customers()

#     subscriptions_df = generate_subscriptions(
#         customers_df
#     )

#     transactions_df = generate_transactions(
#         subscriptions_df
#     )

#     usage_df = generate_product_usage(
#         customers_df
#     )
#     print("\n" + "=" * 60)
#     print("DATA GENERATION COMPLETED")
#     print("=" * 60)

#     print("\nFiles created:")

#     print("1. customers.csv")
#     print("2. subscriptions.csv")
#     print("3. transactions.csv")
#     print("4. product_usage.csv")

#     print("\nRows generated:")

#     print(f"Customers:      {len(customers_df):,}")
#     print(f"Subscriptions:  {len(subscriptions_df):,}")
#     print(f"Transactions:   {len(transactions_df):,}")
#     print(f"Product Usage:  {len(usage_df):,}")

# if __name__ == "__main__":
#     main()

    


import random
from datetime import datetime, timedelta

import pandas as pd

from src.config import RAW_DATA_DIR


# ============================================================
# PROJECT SETTINGS
# ============================================================

NUM_CUSTOMERS = 1000

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)


# ============================================================
# REFERENCE DATA
# ============================================================

INDUSTRIES = [
    "SaaS",
    "FinTech",
    "HealthCare",
    "E-Commerce",
    "Education",
    "Manufacturing",
]

COUNTRIES = [
    "USA",
    "UK",
    "India",
    "Germany",
    "Canada",
    "Australia",
]

ACQUISITION_CHANNELS = [
    "Organic Search",
    "Paid Ads",
    "Referral",
    "LinkedIn",
    "Email",
]

PLANS = {
    "Starter": 99,
    "Growth": 299,
    "Business": 799,
    "Enterprise": 1999,
}

TRANSACTION_TYPES = [
    "new",
    "renewal",
    "upgrade",
    "downgrade",
    "refund",
]

FEATURES = [
    "Dashboard",
    "Reports",
    "Analytics",
    "Automation",
    "API",
    "Integrations",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    days_between = (end_date - start_date).days

    random_days = random.randint(0, days_between)

    return start_date + timedelta(days=random_days)


# ============================================================
# 1. CUSTOMERS
# ============================================================

def generate_customers():
    print("\nGenerating Customers Data...")

    customers = []

    for i in range(1, NUM_CUSTOMERS + 1):

        signup_date = random_date(
            START_DATE,
            datetime(2025, 10, 31)
        )

        customer = {
            "customer_id": f"CUST{i:04d}",
            "company_name": f"Company_{i}",
            "industry": random.choice(INDUSTRIES),
            "country": random.choice(COUNTRIES),
            "signup_date": signup_date.strftime("%Y-%m-%d"),
            "acquisition_channel": random.choice(
                ACQUISITION_CHANNELS
            ),
        }

        customers.append(customer)

    customers_df = pd.DataFrame(customers)

    # --------------------------------------------------------
    # Controlled data-quality issues
    # --------------------------------------------------------

    customers_df.loc[5, "country"] = None

    customers_df.loc[10, "industry"] = None

    customers_df.loc[20, "country"] = "usa"

    customers_df.loc[30, "industry"] = "saas"

    print(customers_df.head())

    customers_df.to_csv(
        RAW_DATA_DIR / "customers.csv",
        index=False
    )

    return customers_df


# ============================================================
# 2. SUBSCRIPTIONS
# ============================================================

def generate_subscriptions(customers_df):
    print("\nGenerating Subscription Data...")

    subscriptions = []

    for i, customer in customers_df.iterrows():

        customer_id = customer["customer_id"]

        start_date = datetime.strptime(
            customer["signup_date"],
            "%Y-%m-%d"
        )

        plan = random.choice(list(PLANS.keys()))

        # Most customers remain active.
        status = random.choice(
            [
                "Active",
                "Active",
                "Active",
                "Active",
                "Cancelled",
            ]
        )

        end_date = None

        if status == "Cancelled":

            possible_end_date = start_date + timedelta(
                days=random.randint(30, 300)
            )

            if possible_end_date <= END_DATE:
                end_date = possible_end_date.strftime("%Y-%m-%d")
            else:
                status = "Active"

        subscription = {
            "subscription_id": f"SUB{i + 1:04d}",
            "customer_id": customer_id,
            "plan": plan,
            "monthly_price": PLANS[plan],
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date,
            "status": status,
        }

        subscriptions.append(subscription)

    subscriptions_df = pd.DataFrame(subscriptions)

    print(subscriptions_df.head())

    subscriptions_df.to_csv(
        RAW_DATA_DIR / "subscriptions.csv",
        index=False
    )

    return subscriptions_df


# ============================================================
# 3. TRANSACTIONS
# ============================================================

def generate_transactions(subscriptions_df):
    print("\nGenerating Transaction Data...")

    transactions = []

    transaction_counter = 1

    for _, subscription in subscriptions_df.iterrows():

        start_date = datetime.strptime(
            subscription["start_date"],
            "%Y-%m-%d"
        )

        end_date = END_DATE

        if pd.notna(subscription["end_date"]):

            end_date = datetime.strptime(
                subscription["end_date"],
                "%Y-%m-%d"
            )

        current_date = start_date

        while current_date <= end_date:

            transaction_type = "renewal"

            if current_date == start_date:
                transaction_type = "new"
            else:
                random_value = random.random()

                if random_value < 0.05:
                    transaction_type = "upgrade"

                elif random_value < 0.10:
                    transaction_type = "downgrade"

                elif random_value < 0.13:
                    transaction_type = "refund"

            amount = subscription["monthly_price"]

            if transaction_type == "upgrade":
                amount = round(amount * 1.5, 2)

            elif transaction_type == "downgrade":
                amount = round(amount * 0.5, 2)

            elif transaction_type == "refund":
                amount = -amount

            transaction = {
                "transaction_id": f"TXN{transaction_counter:06d}",
                "customer_id": subscription["customer_id"],
                "transaction_date": current_date.strftime("%Y-%m-%d"),
                "amount": amount,
                "transaction_type": transaction_type,
            }

            transactions.append(transaction)

            transaction_counter += 1

            # Move to approximately the next month.
            current_date += timedelta(days=30)

    transactions_df = pd.DataFrame(transactions)

    # --------------------------------------------------------
    # Controlled duplicate
    # --------------------------------------------------------

    if len(transactions_df) > 10:
        duplicate_row = transactions_df.iloc[[10]].copy()

        transactions_df = pd.concat(
            [
                transactions_df,
                duplicate_row
            ],
            ignore_index=True
        )

    print(transactions_df.head())

    transactions_df.to_csv(
        RAW_DATA_DIR / "transactions.csv",
        index=False
    )

    return transactions_df


# ============================================================
# 4. PRODUCT USAGE
# ============================================================

def generate_product_usage(customers_df):
    print("\nGenerating Product Usage Data...")

    usage_data = []

    months = pd.date_range(
        start="2025-01-01",
        end="2025-12-01",
        freq="MS"
    )

    for _, customer in customers_df.iterrows():

        customer_id = customer["customer_id"]

        signup_date = datetime.strptime(
            customer["signup_date"],
            "%Y-%m-%d"
        )

        for month in months:

            month_date = month.to_pydatetime()

            # Do not generate usage before signup.
            if month_date < datetime(
                signup_date.year,
                signup_date.month,
                1
            ):
                continue

            active_users = random.randint(1, 50)

            sessions = random.randint(
                active_users,
                active_users * 20
            )

            features_used = random.randint(
                1,
                len(FEATURES)
            )

            usage = {
                "customer_id": customer_id,
                "usage_month": month.strftime("%Y-%m-%d"),
                "active_users": active_users,
                "sessions": sessions,
                "features_used": features_used,
            }

            usage_data.append(usage)

    usage_df = pd.DataFrame(usage_data)

    print(usage_df.head())

    usage_df.to_csv(
        RAW_DATA_DIR / "product_usage.csv",
        index=False
    )

    return usage_df


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print("=" * 60)
    print("B2B SaaS GROWTH ANALYTICS - DATA GENERATION")
    print("=" * 60)

    customers_df = generate_customers()

    subscriptions_df = generate_subscriptions(
        customers_df
    )

    transactions_df = generate_transactions(
        subscriptions_df
    )

    usage_df = generate_product_usage(
        customers_df
    )

    print("\n" + "=" * 60)
    print("DATA GENERATION COMPLETED")
    print("=" * 60)

    print("\nFiles created:")

    print("1. customers.csv")
    print("2. subscriptions.csv")
    print("3. transactions.csv")
    print("4. product_usage.csv")

    print("\nRows generated:")

    print(f"Customers:      {len(customers_df):,}")
    print(f"Subscriptions:  {len(subscriptions_df):,}")
    print(f"Transactions:   {len(transactions_df):,}")
    print(f"Product Usage:  {len(usage_df):,}")


if __name__ == "__main__":
    main()



