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