import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

# -----------------------------
# Project settings
# -----------------------------

NUM_PARTNERS = 800

CITIES = [
    "Delhi NCR",
    "Bengaluru",
    "Mumbai",
    "Pune",
    "Chandigarh"
]

CATEGORIES = [
    "AC & Appliance Repair",
    "Cleaning & Pest Control",
    "Electricians",
    "Plumbers",
    "Beauty & Spa"
]

# -----------------------------
# Generate Partner IDs
# -----------------------------

partner_ids = [
    f"P{i:04d}"
    for i in range(1, NUM_PARTNERS + 1)
]

# -----------------------------
# Generate partner names
# -----------------------------

first_names = [
    "Aarav", "Vikram", "Rahul", "Arjun", "Rohan",
    "Karan", "Amit", "Neeraj", "Sahil", "Varun",
    "Ankit", "Manish", "Ravi", "Nikhil", "Aditya",
    "Priya", "Neha", "Pooja", "Ananya", "Simran"
]

last_names = [
    "Sharma", "Verma", "Patel", "Singh", "Kumar",
    "Gupta", "Mehta", "Malhotra", "Kapoor", "Joshi",
    "Chopra", "Bansal", "Arora", "Sethi", "Mishra"
]

partner_names = [
    f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
    for _ in range(NUM_PARTNERS)
]

# -----------------------------
# Generate cities
# -----------------------------

city_weights = [0.24, 0.24, 0.22, 0.18, 0.12]

cities = np.random.choice(
    CITIES,
    size=NUM_PARTNERS,
    p=city_weights
)

# -----------------------------
# Generate service categories
# -----------------------------

category_weights = [0.22, 0.20, 0.20, 0.18, 0.20]

categories = np.random.choice(
    CATEGORIES,
    size=NUM_PARTNERS,
    p=category_weights
)

# -----------------------------
# Generate join dates
# -----------------------------

start_date = pd.Timestamp("2025-01-01")
end_date = pd.Timestamp("2026-07-31")

days_between = (end_date - start_date).days

join_dates = [
    start_date + pd.Timedelta(
        days=np.random.randint(0, days_between + 1)
    )
    for _ in range(NUM_PARTNERS)
]

# -----------------------------
# Derive experience level
# -----------------------------

today = pd.Timestamp("2026-08-31")

tenure_days = [
    (today - join_date).days
    for join_date in join_dates
]

experience_levels = []

for days in tenure_days:

    if days < 180:
        experience_levels.append("Beginner")

    elif days < 365:
        experience_levels.append("Intermediate")

    else:
        experience_levels.append("Experienced")

# -----------------------------
# Generate initial quality score
# -----------------------------

initial_quality_scores = np.clip(
    np.random.normal(
        loc=78,
        scale=9,
        size=NUM_PARTNERS
    ),
    50,
    98
).round(1)

# -----------------------------
# Generate initial rating
# -----------------------------

initial_ratings = np.clip(
    np.random.normal(
        loc=4.2,
        scale=0.35,
        size=NUM_PARTNERS
    ),
    3.0,
    5.0
).round(1)

# -----------------------------
# Create Partners dataframe
# -----------------------------

partners = pd.DataFrame({
    "Partner_ID": partner_ids,
    "Partner_Name": partner_names,
    "City": cities,
    "Category": categories,
    "Join_Date": join_dates,
    "Experience_Level": experience_levels,
    "Initial_Quality_Score": initial_quality_scores,
    "Initial_Rating": initial_ratings
})

# -----------------------------
# Save dataset
# -----------------------------

partners.to_csv(
    "Data/partners_raw.csv",
    index=False
)

# -----------------------------
# Basic validation
# -----------------------------

print("Partners dataset created successfully.")
print(f"Number of partners: {len(partners)}")
print(f"Unique Partner IDs: {partners['Partner_ID'].nunique()}")

print("\nCity distribution:")
print(partners["City"].value_counts())

print("\nCategory distribution:")
print(partners["Category"].value_counts())

print("\nExperience distribution:")
print(partners["Experience_Level"].value_counts())

print("\nFirst 5 rows:")
print(partners.head())

# ============================================================
# CUSTOMERS DATA
# ============================================================

NUM_CUSTOMERS = 25000

# Generate Customer IDs
customer_ids = [
    f"C{i:05d}"
    for i in range(1, NUM_CUSTOMERS + 1)
]

# Generate customer cities
customer_city_weights = [0.24, 0.24, 0.22, 0.18, 0.12]

customer_cities = np.random.choice(
    CITIES,
    size=NUM_CUSTOMERS,
    p=customer_city_weights
)

# Generate signup dates
customer_start_date = pd.Timestamp("2025-01-01")
customer_end_date = pd.Timestamp("2026-08-31")

customer_days_between = (
    customer_end_date - customer_start_date
).days

signup_dates = [
    customer_start_date + pd.Timedelta(
        days=np.random.randint(
            0,
            customer_days_between + 1
        )
    )
    for _ in range(NUM_CUSTOMERS)
]

# Generate signup channels
signup_channels = [
    "Organic",
    "Referral",
    "Paid Search",
    "Social Media",
    "Other"
]

signup_channel_weights = [
    0.35,
    0.20,
    0.20,
    0.15,
    0.10
]

customer_signup_channels = np.random.choice(
    signup_channels,
    size=NUM_CUSTOMERS,
    p=signup_channel_weights
)

# Create Customers dataframe
customers = pd.DataFrame({
    "Customer_ID": customer_ids,
    "City": customer_cities,
    "Signup_Date": signup_dates,
    "Signup_Channel": customer_signup_channels
})

# Save Customers dataset
customers.to_csv(
    "Data/customers_raw.csv",
    index=False
)

# Basic validation
print("\nCustomers dataset created successfully.")
print(f"Number of customers: {len(customers)}")
print(f"Unique Customer IDs: {customers['Customer_ID'].nunique()}")

print("\nCustomer city distribution:")
print(customers["City"].value_counts())

print("\nSignup channel distribution:")
print(customers["Signup_Channel"].value_counts())

print("\nFirst 5 customers:")
print(customers.head())

# ============================================================
# ORDERS DATA
# ============================================================

NUM_ORDERS = 35000

print("\nStarting Orders dataset generation...")
print(f"Target number of orders: {NUM_ORDERS}")

# -----------------------------
# Generate Order IDs
# -----------------------------

order_ids = [
    f"O{i:05d}"
    for i in range(1, NUM_ORDERS + 1)
]

# -----------------------------
# Select customers for orders
# -----------------------------

order_customer_ids = np.random.choice(
    customers["Customer_ID"],
    size=NUM_ORDERS
)

# Map customer IDs to their cities
customer_city_map = dict(
    zip(
        customers["Customer_ID"],
        customers["City"]
    )
)

order_cities = [
    customer_city_map[customer_id]
    for customer_id in order_customer_ids
]

# -----------------------------
# Generate service categories
# -----------------------------

order_category_weights = [
    0.22,  # AC & Appliance Repair
    0.20,  # Cleaning & Pest Control
    0.20,  # Electricians
    0.18,  # Plumbers
    0.20   # Beauty & Spa
]

order_categories = np.random.choice(
    CATEGORIES,
    size=NUM_ORDERS,
    p=order_category_weights
)

# -----------------------------
# Generate booking dates
# -----------------------------

booking_start_date = pd.Timestamp("2026-01-01")
booking_end_date = pd.Timestamp("2026-08-31")

booking_days_between = (
    booking_end_date - booking_start_date
).days

booking_dates = [
    booking_start_date + pd.Timedelta(
        days=np.random.randint(
            0,
            booking_days_between + 1
        )
    )
    for _ in range(NUM_ORDERS)
]

# -----------------------------
# Create initial Orders dataframe
# -----------------------------

orders = pd.DataFrame({
    "Order_ID": order_ids,
    "Customer_ID": order_customer_ids,
    "City": order_cities,
    "Category": order_categories,
    "Booking_Date": booking_dates
})

print("\nBasic order records generated.")
print(f"Number of orders: {len(orders)}")
print(f"Unique Order IDs: {orders['Order_ID'].nunique()}")

print("\nOrder city distribution:")
print(orders["City"].value_counts())

print("\nOrder category distribution:")
print(orders["Category"].value_counts())

print("\nFirst 5 orders:")
print(orders.head())

# -----------------------------
# Generate scheduled dates
# -----------------------------

scheduled_dates = []

for booking_date in orders["Booking_Date"]:

    # Most services are scheduled within 0–3 days
    delay_days = np.random.choice(
        [0, 1, 2, 3],
        p=[0.35, 0.35, 0.20, 0.10]
    )

    scheduled_dates.append(
        booking_date + pd.Timedelta(days=delay_days)
    )

orders["Scheduled_Date"] = scheduled_dates

# -----------------------------
# Generate partner assignments
# -----------------------------

# -----------------------------
# Generate realistic assignments
# -----------------------------

# Create partner lookup information
partner_lookup = partners.set_index("Partner_ID")

order_partner_ids = []

for _, order in orders.iterrows():

    city = order["City"]
    category = order["Category"]

    # Identify partners operating in the same city and category
    eligible_partners = partners[
        (partners["City"] == city) &
        (partners["Category"] == category)
    ]["Partner_ID"].tolist()

    # If no eligible partner exists, leave order unassigned
    if len(eligible_partners) == 0:
        order_partner_ids.append(None)
        continue

    # Normal assignment probability
    assignment_probability = 0.97

    # Create subtle supply pressure in selected city/category combinations
    if city == "Delhi NCR" and category == "AC & Appliance Repair":
        assignment_probability = 0.90

    elif city == "Mumbai" and category == "Cleaning & Pest Control":
        assignment_probability = 0.92

    elif city == "Bengaluru" and category == "Electricians":
        assignment_probability = 0.93

    # Decide whether the order gets assigned
    if np.random.random() <= assignment_probability:
        order_partner_ids.append(
            np.random.choice(eligible_partners)
        )
    else:
        order_partner_ids.append(None)

orders["Partner_ID"] = order_partner_ids

print("\nRealistic partner assignment completed.")

print(
    "Unassigned orders:",
    orders["Partner_ID"].isna().sum()
)

print(
    "Assignment rate:",
    round(
        orders["Partner_ID"].notna().mean() * 100,
        2
    ),
    "%"
)

print("\nScheduled dates and partner assignments added.")

print("\nOrders preview:")
print(
    orders[
        [
            "Order_ID",
            "Customer_ID",
            "Partner_ID",
            "City",
            "Category",
            "Booking_Date",
            "Scheduled_Date"
        ]
    ].head()
)

# -----------------------------
# Generate order status
# -----------------------------

order_statuses = []

for _, order in orders.iterrows():

    # Unassigned orders cannot be completed
    if pd.isna(order["Partner_ID"]):

        # Most unassigned demand is effectively lost
        order_statuses.append(
            np.random.choice(
                ["Cancelled", "No-Show"],
                p=[0.95, 0.05]
            )
        )

    else:

        # Assigned orders are usually completed
        order_statuses.append(
            np.random.choice(
                ["Completed", "Cancelled", "No-Show"],
                p=[0.88, 0.10, 0.02]
            )
        )

orders["Order_Status"] = order_statuses

print("\nOrder status generated.")

print(
    orders["Order_Status"].value_counts()
)

print(
    "\nOrder status percentages:"
)

print(
    (orders["Order_Status"].value_counts(normalize=True) * 100)
    .round(2)
)

# -----------------------------
# Generate cancellation reasons
# -----------------------------

cancellation_reasons = []

for _, order in orders.iterrows():

    status = order["Order_Status"]
    partner = order["Partner_ID"]

    # Completed and No-Show orders have no cancellation reason
    if status != "Cancelled":
        cancellation_reasons.append("Not Applicable")

    # Unassigned cancellations are primarily supply-related
    elif pd.isna(partner):
        cancellation_reasons.append(
            np.random.choice(
                [
                    "No Partner Available",
                    "Scheduling Conflict",
                    "Other"
                ],
                p=[0.85, 0.10, 0.05]
            )
        )

    # Assigned cancellations
    else:
        cancellation_reasons.append(
            np.random.choice(
                [
                    "Partner Unavailable",
                    "Partner Rejected",
                    "Customer Cancelled",
                    "Scheduling Conflict",
                    "Other"
                ],
                p=[0.25, 0.20, 0.25, 0.20, 0.10]
            )
        )

orders["Cancellation_Reason"] = cancellation_reasons

print("\nCancellation reasons generated.")

print(
    orders["Cancellation_Reason"].value_counts()
)

# -----------------------------
# Generate completion dates
# -----------------------------

completion_dates = []

for _, order in orders.iterrows():

    if order["Order_Status"] == "Completed":

        completion_dates.append(
            order["Scheduled_Date"]
        )

    else:

        completion_dates.append(
            pd.NaT
        )

orders["Completion_Date"] = completion_dates


# -----------------------------
# Generate service duration
# -----------------------------

category_duration_ranges = {
    "AC & Appliance Repair": (60, 180),
    "Cleaning & Pest Control": (60, 240),
    "Electricians": (45, 150),
    "Plumbers": (45, 150),
    "Beauty & Spa": (45, 180)
}

service_durations = []

for _, order in orders.iterrows():

    if order["Order_Status"] == "Completed":

        minimum, maximum = category_duration_ranges[
            order["Category"]
        ]

        duration = np.random.randint(
            minimum,
            maximum + 1
        )

        service_durations.append(duration)

    else:

        service_durations.append(np.nan)

orders["Service_Duration_Min"] = service_durations


# -----------------------------
# Generate response times
# -----------------------------

response_times = []

for _, order in orders.iterrows():

    if pd.isna(order["Partner_ID"]):

        response_times.append(np.nan)

    else:

        response_times.append(
            int(
                np.clip(
                    np.random.normal(
                        loc=30,
                        scale=15
                    ),
                    5,
                    180
                )
            )
        )

orders["Response_Time_Min"] = response_times


print("\nCompletion dates, service duration and response times generated.")

print("\nAverage service duration by category:")
print(
    orders[
        orders["Order_Status"] == "Completed"
    ]
    .groupby("Category")["Service_Duration_Min"]
    .mean()
    .round(1)
)

print("\nAverage response time:")
print(
    round(
        orders["Response_Time_Min"].mean(),
        1
    ),
    "minutes"
)

# -----------------------------
# Generate price
# -----------------------------

category_price_ranges = {
    "AC & Appliance Repair": (400, 2500),
    "Cleaning & Pest Control": (500, 3000),
    "Electricians": (300, 1800),
    "Plumbers": (300, 1800),
    "Beauty & Spa": (600, 3500)
}

prices = []

for _, order in orders.iterrows():

    minimum, maximum = category_price_ranges[
        order["Category"]
    ]

    price = np.random.randint(
        minimum,
        maximum + 1
    )

    prices.append(price)

orders["Price"] = prices


# -----------------------------
# Generate discounts
# -----------------------------

discounts = []

for price in orders["Price"]:

    discount_rate = np.random.choice(
        [0, 0.05, 0.10, 0.15],
        p=[0.45, 0.30, 0.20, 0.05]
    )

    discount = round(
        price * discount_rate,
        2
    )

    discounts.append(discount)

orders["Discount"] = discounts


# -----------------------------
# Generate revenue
# -----------------------------

orders["Revenue"] = np.where(
    orders["Order_Status"] == "Completed",
    orders["Price"] - orders["Discount"],
    0
)

print("\nPrice, discount and revenue generated.")

print("\nAverage price by category:")
print(
    orders
    .groupby("Category")["Price"]
    .mean()
    .round(2)
)

print("\nTotal revenue from completed orders:")
print(
    round(
        orders["Revenue"].sum(),
        2
    )
)

# -----------------------------
# Generate customer ratings
# -----------------------------

customer_ratings = []
complaint_flags = []
rework_flags = []

for _, order in orders.iterrows():

    if order["Order_Status"] == "Completed":

        # Base rating
        rating = np.random.normal(
            loc=4.2,
            scale=0.45
        )

        # High service duration slightly increases
        # probability of quality issues
        if order["Service_Duration_Min"] > 180:
            rating -= 0.15

        rating = round(
            np.clip(rating, 2.5, 5.0),
            1
        )

        customer_ratings.append(rating)

        # Complaint probability
        complaint_probability = 0.06

        if rating < 3.5:
            complaint_probability += 0.12

        if order["Service_Duration_Min"] > 180:
            complaint_probability += 0.04

        complaint_flags.append(
            int(
                np.random.random() < complaint_probability
            )
        )

        # Rework probability
        rework_probability = 0.05

        if rating < 3.5:
            rework_probability += 0.08

        rework_flags.append(
            int(
                np.random.random() < rework_probability
            )
        )

    else:

        # No rating for non-completed orders
        customer_ratings.append(np.nan)
        complaint_flags.append(0)
        rework_flags.append(0)


orders["Customer_Rating"] = customer_ratings
orders["Complaint_Flag"] = complaint_flags
orders["Rework_Flag"] = rework_flags


print("\nCustomer experience metrics generated.")

print("\nAverage customer rating:")
print(
    round(
        orders["Customer_Rating"].mean(),
        2
    )
)

print("\nComplaint rate among completed orders:")
print(
    round(
        orders.loc[
            orders["Order_Status"] == "Completed",
            "Complaint_Flag"
        ].mean() * 100,
        2
    ),
    "%"
)

print("\nRework rate among completed orders:")
print(
    round(
        orders.loc[
            orders["Order_Status"] == "Completed",
            "Rework_Flag"
        ].mean() * 100,
        2
    ),
    "%"
)

# -----------------------------
# Generate assignment status
# -----------------------------

orders["Assignment_Status"] = np.where(
    orders["Partner_ID"].notna(),
    "Assigned",
    "Unassigned"
)


# -----------------------------
# Generate repeat booking flag
# -----------------------------
# For now, initialize this as 0.
# We will derive the actual value from customer
# order history after all orders have been generated.

# -----------------------------
# Derive repeat booking flag
# -----------------------------

# Sort orders by customer and booking date
orders = orders.sort_values(
    ["Customer_ID", "Booking_Date", "Order_ID"]
).reset_index(drop=True)

# Identify whether each customer has another booking
orders["Repeat_Booking_Flag"] = (
    orders.groupby("Customer_ID")["Order_ID"]
    .transform("count")
    .gt(1)
    .astype(int)
)

print("\nRepeat booking flag derived.")

print(
    orders["Repeat_Booking_Flag"].value_counts()
)


print("\nAssignment status generated.")

print(
    orders["Assignment_Status"].value_counts()
)

print("\nRepeat booking flag initialized.")
print(
    orders["Repeat_Booking_Flag"].value_counts()
)

# -----------------------------
# Save complete Orders dataset
# -----------------------------

orders.to_csv(
    "Data/orders_raw.csv",
    index=False
)

print("\nOrders dataset saved successfully.")
print(f"Number of orders: {len(orders)}")
print(f"Number of columns: {len(orders.columns)}")

print("\nOrders columns:")
print(orders.columns.tolist())

# ============================================================
# ONBOARDING DATA
# ============================================================

print("\nStarting Onboarding dataset generation...")

# Use the existing partner IDs
onboarding_partner_ids = partners["Partner_ID"].tolist()

# -----------------------------
# Generate application dates
# -----------------------------

application_start_date = pd.Timestamp("2025-01-01")
application_end_date = pd.Timestamp("2026-07-31")

application_days_between = (
    application_end_date - application_start_date
).days

application_dates = [
    application_start_date + pd.Timedelta(
        days=np.random.randint(
            0,
            application_days_between + 1
        )
    )
    for _ in range(NUM_PARTNERS)
]

# -----------------------------
# Generate verification dates
# -----------------------------

verification_dates = []
verification_statuses = []

for application_date in application_dates:

    # Most partners complete verification
    status = np.random.choice(
        ["Passed", "Failed", "Pending"],
        p=[0.88, 0.07, 0.05]
    )

    verification_statuses.append(status)

    if status == "Pending":

        verification_dates.append(pd.NaT)

    else:

        verification_delay = np.random.randint(1, 8)

        verification_dates.append(
            application_date
            + pd.Timedelta(days=verification_delay)
        )

# -----------------------------
# Create initial Onboarding dataframe
# -----------------------------

onboarding = pd.DataFrame({
    "Partner_ID": onboarding_partner_ids,
    "Application_Date": application_dates,
    "Verification_Date": verification_dates,
    "Verification_Status": verification_statuses
})

print("\nInitial onboarding records generated.")

print(
    f"Number of onboarding records: {len(onboarding)}"
)

print("\nVerification status:")
print(
    onboarding["Verification_Status"].value_counts()
)

print("\nFirst 5 onboarding records:")
print(
    onboarding.head()
)

# -----------------------------
# Generate skill assessment dates
# -----------------------------

skill_assessment_dates = []

for _, row in onboarding.iterrows():

    if row["Verification_Status"] == "Passed":

        delay_days = np.random.randint(2, 8)

        skill_assessment_dates.append(
            row["Verification_Date"]
            + pd.Timedelta(days=delay_days)
        )

    else:

        skill_assessment_dates.append(pd.NaT)

onboarding["Skill_Assessment_Date"] = skill_assessment_dates


# -----------------------------
# Generate training dates/status
# -----------------------------

training_dates = []
training_statuses = []

for _, row in onboarding.iterrows():

    if row["Verification_Status"] != "Passed":

        training_dates.append(pd.NaT)
        training_statuses.append("Pending")

    else:

        training_status = np.random.choice(
            ["Completed", "Pending"],
            p=[0.93, 0.07]
        )

        training_statuses.append(training_status)

        if training_status == "Completed":

            delay_days = np.random.randint(2, 8)

            training_dates.append(
                row["Skill_Assessment_Date"]
                + pd.Timedelta(days=delay_days)
            )

        else:

            training_dates.append(pd.NaT)


onboarding["Training_Date"] = training_dates
onboarding["Training_Status"] = training_statuses


print("\nSkill assessment and training stages generated.")

print("\nTraining status:")
print(
    onboarding["Training_Status"].value_counts()
)
# -----------------------------
# Generate quality check dates
# -----------------------------

quality_check_dates = []
initial_quality_scores = []

for _, row in onboarding.iterrows():

    if row["Training_Status"] == "Completed":

        delay_days = np.random.randint(1, 6)

        quality_check_dates.append(
            row["Training_Date"]
            + pd.Timedelta(days=delay_days)
        )

        # Quality score generated at initial assessment
        score = np.clip(
            np.random.normal(78, 10),
            45,
            98
        )

        initial_quality_scores.append(
            round(score, 1)
        )

    else:

        quality_check_dates.append(pd.NaT)
        initial_quality_scores.append(np.nan)


onboarding["Quality_Check_Date"] = quality_check_dates
onboarding["Initial_Quality_Check"] = initial_quality_scores


# -----------------------------
# Generate activation dates/status
# -----------------------------

activation_dates = []
activation_statuses = []

for _, row in onboarding.iterrows():

    if row["Training_Status"] != "Completed":

        activation_dates.append(pd.NaT)
        activation_statuses.append("In Progress")

    else:

        # Quality check outcome
        quality_result = np.random.choice(
            ["Activated", "Rejected"],
            p=[0.94, 0.06]
        )

        activation_statuses.append(quality_result)

        if quality_result == "Activated":

            delay_days = np.random.randint(1, 5)

            activation_dates.append(
                row["Quality_Check_Date"]
                + pd.Timedelta(days=delay_days)
            )

        else:

            activation_dates.append(pd.NaT)


onboarding["Activation_Date"] = activation_dates
onboarding["Activation_Status"] = activation_statuses


print("\nQuality check and activation stages generated.")

print("\nActivation status:")
print(
    onboarding["Activation_Status"].value_counts()
)
# -----------------------------
# Validate onboarding sequence
# -----------------------------

print("\nOnboarding validation:")

print(
    "Application dates missing:",
    onboarding["Application_Date"].isna().sum()
)

print(
    "Passed verification without verification date:",
    (
        (onboarding["Verification_Status"] == "Passed") &
        (onboarding["Verification_Date"].isna())
    ).sum()
)

print(
    "Activated partners without activation date:",
    (
        (onboarding["Activation_Status"] == "Activated") &
        (onboarding["Activation_Date"].isna())
    ).sum()
)

# -----------------------------
# Save onboarding dataset
# -----------------------------

onboarding.to_csv(
    "Data/onboarding_raw.csv",
    index=False
)

print("\nOnboarding dataset saved successfully.")
print(f"Number of records: {len(onboarding)}")
print(f"Number of columns: {len(onboarding.columns)}")

# ============================================================
# PARTNER AVAILABILITY DATA
# ============================================================

print("\nStarting Partner Availability dataset generation...")

# -----------------------------
# Generate all dates
# -----------------------------

availability_start_date = pd.Timestamp("2026-01-01")
availability_end_date = pd.Timestamp("2026-08-31")

availability_dates = pd.date_range(
    start=availability_start_date,
    end=availability_end_date,
    freq="D"
)

print(f"Number of days: {len(availability_dates)}")


# -----------------------------
# Create Partner x Date grid
# -----------------------------

partner_availability = pd.MultiIndex.from_product(
    [
        partners["Partner_ID"],
        availability_dates
    ],
    names=["Partner_ID", "Date"]
).to_frame(index=False)

print(
    f"Initial availability records: {len(partner_availability)}"
)


# -----------------------------
# Add partner information
# -----------------------------

partner_information = partners[
    [
        "Partner_ID",
        "City",
        "Category",
        "Experience_Level"
    ]
].copy()

partner_availability = partner_availability.merge(
    partner_information,
    on="Partner_ID",
    how="left"
)


# ============================================================
# GENERATE AVAILABLE HOURS
# ============================================================

available_hours = []

for _, row in partner_availability.iterrows():

    partner_id = row["Partner_ID"]
    date = row["Date"]

    # Find partner experience
    experience = row["Experience_Level"]

    # Weekend effect
    is_weekend = date.dayofweek >= 5

    # Base availability
    if experience == "Beginner":
        base_hours = 7.0

    elif experience == "Intermediate":
        base_hours = 8.0

    else:
        base_hours = 8.5

    # Slightly lower availability on weekends
    if is_weekend:
        base_hours -= 1.5

    # Random daily variation
    hours = np.random.normal(
        loc=base_hours,
        scale=1.5
    )

    # Some days partners are unavailable
    unavailable_probability = 0.08

    if np.random.random() < unavailable_probability:
        hours = 0

    else:
        hours = np.clip(
            hours,
            2,
            12
        )

    available_hours.append(
        round(hours, 1)
    )


partner_availability["Available_Hours"] = available_hours


# ============================================================
# AVAILABILITY STATUS
# ============================================================

partner_availability["Availability_Status"] = np.where(
    partner_availability["Available_Hours"] > 0,
    "Available",
    "Unavailable"
)


# ============================================================
# CALCULATE BOOKED HOURS FROM COMPLETED ORDERS
# ============================================================

# Only completed orders contribute to booked service hours
completed_orders = orders[
    orders["Order_Status"] == "Completed"
].copy()

# Make sure completion date is treated as a date
completed_orders["Completion_Date"] = pd.to_datetime(
    completed_orders["Completion_Date"]
)

# Convert service duration from minutes to hours
completed_orders["Booked_Hours"] = (
    completed_orders["Service_Duration_Min"] / 60
)

# Aggregate completed service hours
# by Partner + Completion Date
booked_hours = (
    completed_orders
    .groupby(
        [
            "Partner_ID",
            "Completion_Date"
        ],
        as_index=False
    )["Booked_Hours"]
    .sum()
)

# Rename date so it matches availability table
booked_hours = booked_hours.rename(
    columns={
        "Completion_Date": "Date"
    }
)


# ============================================================
# MERGE BOOKED HOURS
# ============================================================

partner_availability = partner_availability.merge(
    booked_hours,
    on=["Partner_ID", "Date"],
    how="left"
)

# Partners with no completed services that day
# have zero booked hours
partner_availability["Booked_Hours"] = (
    partner_availability["Booked_Hours"]
    .fillna(0)
)


# ============================================================
# CAP BOOKED HOURS AT AVAILABLE HOURS
# ============================================================

# A partner cannot be considered booked for more hours
# than they were available.
partner_availability["Booked_Hours"] = np.minimum(
    partner_availability["Booked_Hours"],
    partner_availability["Available_Hours"]
)

partner_availability["Booked_Hours"] = (
    partner_availability["Booked_Hours"]
    .round(2)
)


# ============================================================
# KEEP ONLY REQUIRED DATA-DICTIONARY COLUMNS
# ============================================================

partner_availability = partner_availability[
    [
        "Date",
        "Partner_ID",
        "Available_Hours",
        "Booked_Hours",
        "Availability_Status"
    ]
]


# ============================================================
# VALIDATION
# ============================================================

print("\nPartner Availability dataset generated.")

print(
    f"Number of records: {len(partner_availability)}"
)

print(
    f"Expected records: "
    f"{NUM_PARTNERS * len(availability_dates)}"
)

print(
    f"Number of columns: "
    f"{len(partner_availability.columns)}"
)

print("\nAvailability status:")
print(
    partner_availability[
        "Availability_Status"
    ].value_counts()
)

print("\nAvailable hours summary:")
print(
    partner_availability[
        "Available_Hours"
    ].describe()
)

print("\nBooked hours summary:")
print(
    partner_availability[
        "Booked_Hours"
    ].describe()
)

print("\nRecords where booked hours exceed available hours:")

print(
    (
        partner_availability["Booked_Hours"]
        > partner_availability["Available_Hours"]
    ).sum()
)


# ============================================================
# SAVE CSV
# ============================================================

partner_availability.to_csv(
    "Data/partner_availability_raw.csv",
    index=False
)

print(
    "\nPartner Availability CSV saved successfully."
)