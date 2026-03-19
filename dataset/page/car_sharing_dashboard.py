import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Car Sharing Dashboard", layout="wide")
st.title("Car Sharing Dashboard")
BASE_DIR = os.path.dirname(__file__)

@st.cache_data
def load_data():

    trips = pd.read_csv(os.path.join(BASE_DIR, "../trips.csv"))
    cars = pd.read_csv(os.path.join(BASE_DIR, "../cars.csv"))
    cities = pd.read_csv(os.path.join(BASE_DIR, "../cities.csv"))

    return trips, cars, cities


trips, cars, cities = load_data()
trips_merged = trips.merge(
    cars,
    left_on="car_id",
    right_on="id_car"
)

trips_merged = trips_merged.merge(
    cities,
    left_on="city_id",
    right_on="id_city"
)
trips_merged = trips_merged.drop(
    columns=["id_car", "city_id", "id_customer", "id"]
)
trips_merged["pickup_time"] = pd.to_datetime(
    trips_merged["pickup_time"]
)

trips_merged["pickup_date"] = (
    trips_merged["pickup_time"].dt.date
)trips_merged["pickup_time"] = pd.to_datetime(
    trips_merged["pickup_time"]
)

trips_merged["pickup_date"] = (
    trips_merged["pickup_time"].dt.date
)
st.sidebar.header("Filter")

cars_brand = st.sidebar.multiselect(
    "Select the Car Brand",
    trips_merged["brand"].unique()
)

if len(cars_brand) > 0:

    trips_merged = trips_merged[
        trips_merged["brand"].isin(cars_brand)
    ]
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
    st.metric("Total Trips", total_trips)

with col2:
    st.metric("Top Car Model", top_car)

with col3:
    st.metric(
        "Total Distance",
        f"{total_distance:,.2f}"
    )
