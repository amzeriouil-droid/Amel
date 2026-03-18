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
    import streamlit as st
import pandas as pd

# Configuration de la page (Optionnel mais recommandé)
st.set_page_config(page_title="Car Sharing Analytics", layout="wide")
st.title("🚗 Dashboard d'Analyse Car Sharing")

# --- 1. CHARGEMENT DES DONNÉES (Requirement Page 1) ---
@st.cache_data
def load_data():
    # Chargement depuis ton dossier 'Dataset'
    trips = pd.read_csv("Dataset/trips.csv")
    cars = pd.read_csv("Dataset/cars.csv")
    cities = pd.read_csv("Dataset/cities.csv")
    return trips, cars, cities

try:
    trips, cars, cities = load_data()

    # --- 2. FUSION DES DONNÉES (Requirement Page 1 & 2) ---
    # Merge trips with cars
    trips_merged = trips.merge(cars, left_on='car_id', right_on='id_car')
    # Merge with cities
    trips_merged = trips_merged.merge(cities, left_on='city_id', right_on='id_city')

    # --- 3. NETTOYAGE DES COLONNES (Requirement Page 2) ---
    trips_merged = trips_merged.drop(columns=["id_car", "city_id", "id_customer", "id"])

    # --- 4. FORMATAGE DES DATES (Requirement Page 2) ---
    trips_merged['pickup_time'] = pd.to_datetime(trips_merged['pickup_time'])
    trips_merged['pickup_date'] = trips_merged['pickup_time'].dt.date

    # --- 5. FILTRES (Requirement Page 3) ---
    st.sidebar.header("Filtres")
    brands = sorted(trips_merged['brand'].unique())
    selected_brands = st.sidebar.multiselect("Sélectionnez les marques", brands, default=brands)

    # Filtrage du tableau principal
    df_filtered = trips_merged[trips_merged['brand'].isin(selected_brands)]

    # --- 6. MÉTRIQUES (Requirement Page 3) ---
    st.header(" Indicateurs Clés")
    col1, col2, col3 = st.columns(3)
    
    total_trips = len(df_filtered)
    total_distance = df_filtered['distance'].sum()
    top_car = df_filtered.groupby('model')['revenue'].sum().idxmax()

    with col1:
        st.metric(label="Total Trajets", value=total_trips)
    with col2:
        st.metric(label="Modèle le plus Rentable", value=top_car)
    with col3:
        st.metric(label="Distance Totale (km)", value=f"{total_distance:,.2f}")

    # --- 7. VISUALISATIONS (Requirement Page 4) ---
    st.divider()
    st.header(" Analyses Graphiques")

    c1, c2 = st.columns(2)

    with c1:
        # 1. Trips Over Time (Line Chart)
        st.subheader("Nombre de trajets par jour")
        trips_day = df_filtered.groupby('pickup_date').size()
        st.line_chart(trips_day)

        # 2. Number of Trips Per Car Model (Bar Chart)
        st.subheader("Trajets par modèle")
        st.bar_chart(df_filtered['model'].value_counts())

    with c2:
        # 3. Revenue by City (Area Chart)
        st.subheader("Revenu total par ville")
        rev_city = df_filtered.groupby('city_name')['revenue'].sum()
        st.area_chart(rev_city)

        # BONUS : Visualisation personnalisée (Distance moyenne par ville)
        st.subheader(" Bonus : Distance moyenne par ville")
        avg_dist_city = df_filtered.groupby('city_name')['distance'].mean()
        st.bar_chart(avg_dist_city)

    # Aperçu des données final demandé
    st.divider()
    st.subheader("Aperçu des données (Preview)")
    st.write(df_filtered.head(10))

except Exception as e:
    st.error(f"Erreur : {e}")
    st.info("Vérifiez que vos fichiers CSV sont bien dans le dossier 'Dataset'.")