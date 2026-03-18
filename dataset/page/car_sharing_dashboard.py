import streamlit as st
import pandas as pd

st.set_page_config(page_title="Car Sharing Dashboard", layout="wide")
st.title("🚗 Car Sharing Analytics")

# Function to load CSV files into dataframes
@st.cache_data
def load_data(): 
    trips = pd.read_csv("data/trips.csv") 
    cars = pd.read_csv("data/cars.csv") 
    cities = pd.read_csv("data/cities.csv") 
    return trips, cars, cities


# Load data
trips, cars, cities = load_data()


# Merge trips with cars (joining on car_id)
trips_merged = trips.merge(
    cars,
    left_on="car_id",
    right_on="id_car"
)


# Merge with cities for car's city (joining on city_id)
trips_merged = trips_merged.merge(
    cities,
    left_on="city_id",
    right_on="id_city"
)


# Drop useless columns
trips_merged = trips_merged.drop(
    columns=["id_car", "city_id", "id_customer", "id"]
)


# Convert date
trips_merged["pickup_time"] = pd.to_datetime(trips_merged["pickup_time"])
trips_merged["pickup_date"] = trips_merged["pickup_time"].dt.date


# -----------------------------
# FILTER SIDEBAR
# -----------------------------

st.sidebar.header("Filters")

cars_brand = st.sidebar.multiselect(
    "Select the Car Brand",
    trips_merged["brand"].unique()
)

if len(cars_brand) > 0:
    trips_merged = trips_merged[
        trips_merged["brand"].isin(cars_brand)
    ]


# -----------------------------
# METRICS
# -----------------------------

total_trips = len(trips_merged)

total_distance = trips_merged["distance"].sum()

top_car = (
    trips_merged
    .groupby("model")["revenue"]
    .sum()
    .idxmax()
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Trips", value=total_trips)

with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)

with col3:
    st.metric(
        label="Total Distance (km)",
        value=f"{total_distance:,.2f}"
    )


# -----------------------------
# VISUALIZATIONS
# -----------------------------

st.divider()
st.header("Charts")

c1, c2 = st.columns(2)

with c1:

    st.subheader("Trips Over Time")
    trips_day = trips_merged.groupby("pickup_date").size()
    st.line_chart(trips_day)

    st.subheader("Trips per Model")
    st.bar_chart(
        trips_merged["model"].value_counts()
    )

with c2:

    st.subheader("Revenue by City")
    rev_city = trips_merged.groupby("city_name")["revenue"].sum()
    st.area_chart(rev_city)

    st.subheader("Average Distance by City (Bonus)")
    avg_dist = trips_merged.groupby("city_name")["distance"].mean()
    st.bar_chart(avg_dist)


# -----------------------------
# PREVIEW
# -----------------------------

st.divider()
st.subheader("Preview Data")

st.write(trips_merged.head())