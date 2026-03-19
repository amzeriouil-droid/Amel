import streamlit as st
import pandas as pd

st.title("🚗 Car Sharing Dashboard")

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    trips  = pd.read_csv("data/trips.csv")
    cars   = pd.read_csv("data/cars.csv")
    cities = pd.read_csv("data/cities.csv")
    return trips, cars, cities

trips, cars, cities = load_data()

# ── 2. MERGE ──────────────────────────────────────────────────────────────────
# trips ← cars (trip references car_id → cars.id)
trips_merged = trips.merge(cars, left_on="car_id", right_on="id", suffixes=("", "_car"))

# trips_merged ← cities (cars references city_id → cities.city_id)
trips_merged = trips_merged.merge(cities, on="city_id", suffixes=("", "_city"))

# ── 3. DROP USELESS COLUMNS ───────────────────────────────────────────────────
trips_merged = trips_merged.drop(
    columns=["id", "city_id", "customer_id", "car_id"],
    errors="ignore"
)

# ── 4. FIX DATE FORMAT ────────────────────────────────────────────────────────
trips_merged["pickup_date"]  = pd.to_datetime(trips_merged["pickup_time"]).dt.date
trips_merged["dropoff_date"] = pd.to_datetime(trips_merged["dropoff_time"]).dt.date

# ── 5. SIDEBAR FILTERS ────────────────────────────────────────────────────────
st.sidebar.header("Filters")
cars_brand = st.sidebar.multiselect(
    "Select the Car Brand",
    options=trips_merged["brand"].unique(),
    default=trips_merged["brand"].unique()
)

trips_merged = trips_merged[trips_merged["brand"].isin(cars_brand)]

# ── 6. BUSINESS METRICS ───────────────────────────────────────────────────────
total_trips    = len(trips_merged)
total_distance = trips_merged["distance"].sum()
top_car        = trips_merged.groupby("model")["revenue"].sum().idxmax()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Trips", value=total_trips)
with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)
with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

# ── 7. PREVIEW DATAFRAME ──────────────────────────────────────────────────────
st.subheader("Data Preview")
st.write(trips_merged.head())

# ── 8. VISUALIZATIONS ─────────────────────────────────────────────────────────

# 8a. Trips Over Time
st.subheader("📅 Trips Over Time")
trips_over_time = (
    trips_merged.groupby("pickup_date")
    .size()
    .reset_index(name="trips")
    .set_index("pickup_date")
)
st.line_chart(trips_over_time)

# 8b. Revenue Per Car Model
st.subheader("💰 Revenue per Car Model")
revenue_per_model = (
    trips_merged.groupby("model")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
st.bar_chart(revenue_per_model)

# 8c. Cumulative Revenue Growth Over Time
st.subheader("📈 Cumulative Revenue Growth Over Time")
cumulative_revenue = (
    trips_merged.groupby("pickup_date")["revenue"]
    .sum()
    .cumsum()
    .reset_index()
    .set_index("pickup_date")
)
st.area_chart(cumulative_revenue)

# 8d. Number of Trips Per Car Model
st.subheader("🚘 Number of Trips per Car Model")
trips_per_model = (
    trips_merged.groupby("model")
    .size()
    .sort_values(ascending=False)
)
st.bar_chart(trips_per_model)

# 8e. Revenue by City
st.subheader("🏙️ Revenue by City")
revenue_by_city = (
    trips_merged.groupby("city_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
st.bar_chart(revenue_by_city)