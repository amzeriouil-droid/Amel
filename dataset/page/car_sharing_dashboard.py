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