import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from psycopg2.extras import execute_values

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432"),
}

def get_database_connection():
    return psycopg2.connect(**DB_CONFIG)

def fetch_earthquake_data(conn):
    """Fetch earthquake id, latitude, longitude from DB."""
    query = """
    SELECT id, latitude, longitude FROM earthquakes
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

    cluster_sizes = np.bincount(labels)

    return centroids, labels, cluster_sizes

def store_clusters(clusters, conn):
    """Insert or overwrite cluster centroids into earthquake_clusters table."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM earthquake_clusters;")
        insert_query = """
        INSERT INTO earthquake_clusters (latitude, longitude, cluster_size)
        VALUES %s
        RETURNING id;
        """
        values = [(float(c[0]), float(c[1]), int(size)) for c, size in clusters]
        execute_values(cur, insert_query, values)
        cluster_ids = [row[0] for row in cur.fetchall()]
        conn.commit()
    return cluster_ids

def update_earthquake_cluster_ids(conn, earthquake_ids, cluster_labels, cluster_ids):
    """
    Update earthquakes table, setting cluster_id based on KMeans labels.
    earthquake_ids: list of earthquake ids
    cluster_labels: list of cluster index for each earthquake
    cluster_ids: list of cluster ids from DB (in same order as clusters)
    """
    with conn.cursor() as cur:
        # Prepare list of tuples (cluster_id, earthquake_id)
        update_values = [(cluster_ids[label], eq_id) for eq_id, label in zip(earthquake_ids, cluster_labels)]
        update_query = """
        UPDATE earthquakes SET cluster_id = data.cluster_id
        FROM (VALUES %s) AS data(cluster_id, id)
        WHERE earthquakes.id = data.id;
        """
        execute_values(cur, update_query, update_values)
        conn.commit()

if __name__ == "__main__":
    conn = get_database_connection()

    df = fetch_earthquake_data(conn)
    if df.empty:
        print("No earthquake data found.")
    else:
        print(f"Clustering {len(df)} earthquake points...")

        centroids, labels, cluster_sizes = run_kmeans(df, n_clusters=5)

        clusters_data = list(zip(centroids, cluster_sizes))

        # Store clusters in DB and get their assigned IDs
        cluster_ids = store_clusters(clusters_data, conn)

        # Update each earthquake's cluster_id
        update_earthquake_cluster_ids(conn, df['id'].tolist(), labels, cluster_ids)

        print(f"Inserted {len(cluster_ids)} clusters and updated earthquakes with cluster IDs.")

    conn.close()
