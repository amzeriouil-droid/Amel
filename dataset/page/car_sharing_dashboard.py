# Function to load CSV files into dataframes
@st.cache_data
def load_data(): 
    trips = pd.read_csv("data/trips.csv") 
    cars = pd.read_csv("data/cars.csv") 
    cities = pd.read_csv("data/cities.csv") 
return trips, cars, cities 
# Merge trips with cars (joining on car_id) 
trips_merged = trips.merge(TO COMPLETE) 
# Merge with cities for car's city (joining on city_id) 
trips_merged = trips_merged.merge(TO COMPLETE)
trips_merged = trips_merged.drop(columns=["id_car", "city_id", "id_customer", 
"id"])
df['pickup_date'] = pd.to_datetime(df['pickup_time']).dt.date 
df['pickup_date'] = pd.to_datetime(df['pickup_time']).dt.date
cars_brand = st.sidebar.multiselect("Select the Car Brand", TO COMPLETE) 
trips_merged = trips_merged[TO COMPLETE] 
# Compute business performance metrics 
total_trips = TO COMPLETE  # Total number of trips 
total_distance = TO COMPLETE  # Sum of all trip distances
# Car model with the highest revenue 
top_car = TO COMPLETE 
# Display metrics in columns 
col1, col2, col3 = st.columns(3) 
with col1: 
    st.metric(label="Total Trips", value=total_trips) 
with col2: 
    st.metric(label="Top Car Model by Revenue", value=top_car) 
with col3: 
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}") 