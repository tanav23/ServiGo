import pandas as pd
import os

# -----------------------------
# File locations
# -----------------------------
DATA_FOLDER = "Data"

files = {
    "partners": "partners_raw.csv",
    "customers": "customers_raw.csv",
    "orders": "orders_raw.csv",
    "onboarding": "onboarding_raw.csv",
    "partner_availability": "partner_availability_raw.csv"
}

# -----------------------------
# Load data
# -----------------------------
print("\n========== SERVIGO DATA VALIDATION ==========\n")

data = {}

for name, filename in files.items():
    filepath = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(filepath):
        print(f"ERROR: {filename} not found.")
        continue

    df = pd.read_csv(filepath)
    data[name] = df

    print(f"{filename}: {len(df):,} rows | {len(df.columns)} columns")


# -----------------------------
# 1. Missing-value check
# -----------------------------
print("\n========== MISSING VALUES ==========\n")

for name, df in data.items():
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    print(f"\n{name.upper()}")

    if len(missing) == 0:
        print("No missing values.")
    else:
        print(missing)


# -----------------------------
# 2. Duplicate check
# -----------------------------
print("\n========== DUPLICATE CHECK ==========\n")

primary_keys = {
    "partners": "Partner_ID",
    "customers": "Customer_ID",
    "orders": "Order_ID",
    "onboarding": "Partner_ID"
}

for name, key in primary_keys.items():
    df = data[name]

    duplicates = df[key].duplicated().sum()

    print(f"{name}: {duplicates:,} duplicate {key} values")


# Partner availability should have
# one row per Partner + Date
if "partner_availability" in data:
    df = data["partner_availability"]

    duplicates = df.duplicated(
        subset=["Partner_ID", "Date"]
    ).sum()

    print(
        f"partner_availability: "
        f"{duplicates:,} duplicate Partner_ID + Date combinations"
    )


# -----------------------------
# 3. Required column check
# -----------------------------
print("\n========== COLUMN CHECK ==========\n")

required_columns = {
    "partners": [
        "Partner_ID",
        "Partner_Name",
        "City",
        "Category",
        "Join_Date",
        "Experience_Level",
        "Onboarding_Status",
        "Training_Status",
        "Active_Status",
        "Initial_Quality_Score",
        "Initial_Rating"
    ],

    "customers": [
        "Customer_ID",
        "City",
        "Signup_Date",
        "Customer_Segment",
        "Signup_Channel"
    ],

    "orders": [
        "Order_ID",
        "Customer_ID",
        "Partner_ID",
        "City",
        "Category",
        "Booking_Date",
        "Scheduled_Date",
        "Completion_Date",
        "Order_Status",
        "Cancellation_Reason",
        "Customer_Rating",
        "Service_Duration_Min",
        "Response_Time_Min",
        "Price",
        "Discount",
        "Revenue",
        "Complaint_Flag",
        "Rework_Flag",
        "Repeat_Booking_Flag",
        "Assignment_Status"
    ],

    "onboarding": [
        "Partner_ID",
        "Application_Date",
        "Verification_Date",
        "Skill_Assessment_Date",
        "Training_Date",
        "Quality_Check_Date",
        "Activation_Date",
        "Verification_Status",
        "Training_Status",
        "Initial_Quality_Check",
        "Activation_Status"
    ],

    "partner_availability": [
        "Date",
        "Partner_ID",
        "Available_Hours",
        "Booked_Hours",
        "Availability_Status"
    ]
}

for name, columns in required_columns.items():

    if name not in data:
        continue

    actual_columns = set(data[name].columns)

    missing_columns = [
        col for col in columns
        if col not in actual_columns
    ]

    if missing_columns:
        print(f"{name}: MISSING COLUMNS")
        print(missing_columns)
    else:
        print(f"{name}: All required columns present")


# -----------------------------
# 4. Referential integrity
# -----------------------------
print("\n========== REFERENTIAL INTEGRITY ==========\n")

partners = data["partners"]
customers = data["customers"]
orders = data["orders"]
onboarding = data["onboarding"]
availability = data["partner_availability"]

partner_ids = set(partners["Partner_ID"])
customer_ids = set(customers["Customer_ID"])

# Orders → Partners
invalid_order_partners = orders[
    orders["Partner_ID"].notna() &
    ~orders["Partner_ID"].isin(partner_ids)
]

print(
    "Orders with invalid Partner_ID:",
    len(invalid_order_partners)
)

# Orders → Customers
invalid_order_customers = orders[
    ~orders["Customer_ID"].isin(customer_ids)
]

print(
    "Orders with invalid Customer_ID:",
    len(invalid_order_customers)
)

# Onboarding → Partners
invalid_onboarding_partners = onboarding[
    ~onboarding["Partner_ID"].isin(partner_ids)
]

print(
    "Onboarding with invalid Partner_ID:",
    len(invalid_onboarding_partners)
)

# Availability → Partners
invalid_availability_partners = availability[
    ~availability["Partner_ID"].isin(partner_ids)
]

print(
    "Availability with invalid Partner_ID:",
    len(invalid_availability_partners)
)


# -----------------------------
# 5. Business-rule validation
# -----------------------------
print("\n========== BUSINESS RULE CHECKS ==========\n")

# Orders
completed = orders["Order_Status"] == "Completed"

print(
    "Completed orders without Partner_ID:",
    ((completed) & (orders["Partner_ID"].isna())).sum()
)

print(
    "Completed orders without Completion_Date:",
    ((completed) & (orders["Completion_Date"].isna())).sum()
)

print(
    "Non-completed orders with Revenue:",
    (
        (~completed) &
        (orders["Revenue"] > 0)
    ).sum()
)

print(
    "Orders where Revenue > Price:",
    (orders["Revenue"] > orders["Price"]).sum()
)

print(
    "Orders where Discount > Price:",
    (orders["Discount"] > orders["Price"]).sum()
)

print(
    "Orders where Booked/Completion data is inconsistent:",
    (
        (completed & orders["Service_Duration_Min"].isna())
    ).sum()
)


# -----------------------------
# 6. Availability validation
# -----------------------------
print("\n========== AVAILABILITY CHECK ==========\n")

print(
    "Records where Booked_Hours > Available_Hours:",
    (
        availability["Booked_Hours"] >
        availability["Available_Hours"]
    ).sum()
)

print(
    "Negative Available_Hours:",
    (availability["Available_Hours"] < 0).sum()
)

print(
    "Negative Booked_Hours:",
    (availability["Booked_Hours"] < 0).sum()
)


# -----------------------------
# 7. Status distribution
# -----------------------------
print("\n========== STATUS DISTRIBUTIONS ==========\n")

print("Order Status:")
print(orders["Order_Status"].value_counts())

print("\nAssignment Status:")
print(orders["Assignment_Status"].value_counts())

print("\nVerification Status:")
print(onboarding["Verification_Status"].value_counts())

print("\nTraining Status:")
print(onboarding["Training_Status"].value_counts())

print("\nActivation Status:")
print(onboarding["Activation_Status"].value_counts())


# -----------------------------
# 8. Date validation
# -----------------------------
print("\n========== DATE RANGE CHECK ==========\n")

orders["Booking_Date"] = pd.to_datetime(
    orders["Booking_Date"]
)

orders["Scheduled_Date"] = pd.to_datetime(
    orders["Scheduled_Date"]
)

print(
    "Order booking date:",
    orders["Booking_Date"].min().date(),
    "to",
    orders["Booking_Date"].max().date()
)

print(
    "Order scheduled date:",
    orders["Scheduled_Date"].min().date(),
    "to",
    orders["Scheduled_Date"].max().date()
)


# -----------------------------
# Final message
# -----------------------------
print("\n============================================")
print("VALIDATION COMPLETE")
print("============================================\n")