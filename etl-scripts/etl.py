import requests
import pandas as pd
import psycopg2
import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv


load_dotenv()  # Load variables from .env into environment


def fetch_earthquake_data():
    
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    
    # Send GET request to USGS API
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request failed
    
    data = response.json()
    
    # Extract 'features' which contains earthquake data points
    features = data['features']
    
    records = []
    for feature in features:
        props = feature['properties']
        geom = feature['geometry']
        # Create a dictionary for each earthquake record
        record = {
            'id': feature['id'],  # unique earthquake ID
            'time': pd.to_datetime(props['time'], unit='ms'),  # convert from ms timestamp
            'latitude': geom['coordinates'][1],  # latitude
            'longitude': geom['coordinates'][0],  # longitude
            'depth': geom['coordinates'][2],  # depth in km
            'magnitude': props['mag'],  # earthquake magnitude
            'place': props['place']  # human-readable location
        }
        records.append(record)
    
    # Convert list of dicts into a DataFrame for easy manipulation
    df = pd.DataFrame(records)
    return df


def insert_earthquakes(df, conn):
    """
    Inserts earthquake records from the DataFrame into the PostgreSQL database.
    Uses batch insert with 'ON CONFLICT' to avoid duplicate primary keys,
    updating existing records if necessary.
    """
    insert_query = """
    INSERT INTO earthquakes (id, time, latitude, longitude, depth, magnitude, place)
    VALUES %s
    ON CONFLICT (id) DO UPDATE SET
        time = EXCLUDED.time,
        latitude = EXCLUDED.latitude,
        longitude = EXCLUDED.longitude,
        depth = EXCLUDED.depth,
        magnitude = EXCLUDED.magnitude,
        place = EXCLUDED.place;
    """
    
    # Convert DataFrame rows to list of tuples for batch insert
    records = list(df.itertuples(index=False, name=None))
    
    with conn.cursor() as cur:
        # execute_values efficiently inserts many rows at once
        execute_values(cur, insert_query, records)
        conn.commit()  # commit transaction


if __name__ == "__main__":
    # Fetch earthquake data into DataFrame
    df = fetch_earthquake_data()
    print(df.head())  # print first few rows for verification
    
    # connect to postgresql database
    conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
    )

    
    # Insert data into the earthquakes table
    insert_earthquakes(df, conn)
    
    # Close DB connection
    conn.close()
