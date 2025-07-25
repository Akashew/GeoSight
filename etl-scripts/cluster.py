import os
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from psycopg2.extras import execute_values

# Load environment variables from .env file
load_dotenv()

def get_database_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def fetch_earthquake_data(conn):
    """Fetch latitude and longitude of earthquakes from DB."""
    query = """
    SELECT latitude, longitude FROM earthquakes
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
    """
    df = pd.read_sql(query, conn)
    return df

def run_kmeans(df, n_clusters=5):
    """Run K-means clustering and return centroids and cluster sizes."""
    coords = df[['latitude', 'longitude']].to_numpy()
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(coords)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    # Count how many points per cluster
    cluster_sizes = np.bincount(labels)

    return [
        {
            'latitude': float(lat),
            'longitude': float(lon),
            'cluster_size': int(size)
        }
        for (lat, lon), size in zip(centroids, cluster_sizes)
    ]

def store_clusters(clusters, conn):
    """Insert or overwrite cluster centroids into earthquake_clusters table."""
    # Optional: Clear old clusters before inserting new ones
    with conn.cursor() as cur:
        cur.execute("DELETE FROM earthquake_clusters;")
        insert_query = """
        INSERT INTO earthquake_clusters (latitude, longitude, cluster_size)
        VALUES %s;
        """
        values = [(c['latitude'], c['longitude'], c['cluster_size']) for c in clusters]
        execute_values(cur, insert_query, values)
        conn.commit()

if __name__ == "__main__":
    conn = get_database_connection()

    
    df = fetch_earthquake_data(conn)
    if df.empty:
        print("No earthquake data found.")
    else:
        print(f"Clustering {len(df)} earthquake points...")

        clusters = run_kmeans(df, n_clusters=5)

        # Step 3: Store in DB
        store_clusters(clusters, conn)
        print(f"Inserted {len(clusters)} clusters into database.")

    conn.close()
