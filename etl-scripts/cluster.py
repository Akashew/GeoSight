import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
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

def find_optimal_clusters_elbow(coords, max_k=20):
    """Find optimal number of clusters using elbow method."""
    distortions = []
    k_range = range(2, min(max_k + 1, len(coords) // 10)) 
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(coords)
        distortions.append(kmeans.inertia_)
    
    # Simple elbow detection - find the point where improvement slows down
    diffs = np.diff(distortions)
    diff_ratios = diffs[:-1] / diffs[1:]
    optimal_k = k_range[np.argmax(diff_ratios) + 1]
    
    return optimal_k, k_range, distortions

def find_optimal_clusters_silhouette(coords, max_k=15):
    """Find optimal number of clusters using silhouette score."""
    silhouette_scores = []
    k_range = range(2, min(max_k + 1, len(coords) // 20))
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        cluster_labels = kmeans.fit_predict(coords)
        silhouette_avg = silhouette_score(coords, cluster_labels)
        silhouette_scores.append(silhouette_avg)
    
    optimal_k = k_range[np.argmax(silhouette_scores)]
    return optimal_k, k_range, silhouette_scores

def run_kmeans_optimal(df, method='adaptive'):
    """Run K-means clustering with optimal number of clusters."""
    coords = df[['latitude', 'longitude']].to_numpy()
    
    if method == 'elbow':
        optimal_k, _, _ = find_optimal_clusters_elbow(coords)
        print(f"Elbow method suggests {optimal_k} clusters")
    elif method == 'silhouette':
        optimal_k, _, _ = find_optimal_clusters_silhouette(coords)
        print(f"Silhouette method suggests {optimal_k} clusters")
    elif method == 'adaptive':
        # Adaptive approach based on data size
        n_points = len(coords)
        if n_points < 1000:
            optimal_k = max(3, n_points // 100)
        elif n_points < 5000:
            optimal_k = max(8, n_points // 300)
        elif n_points < 15000:
            optimal_k = max(15, n_points // 500)
        else:
            optimal_k = max(20, min(50, n_points // 800))
        print(f"Adaptive method suggests {optimal_k} clusters for {n_points} earthquakes")
    else:
        # Fixed number (your original approach)
        optimal_k = 5
    
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    kmeans.fit(coords)
    
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    cluster_sizes = np.bincount(labels)
    
    return centroids, labels, cluster_sizes

def run_dbscan_clustering(df, eps=1.0, min_samples=10):
    """Alternative: Use DBSCAN for density-based clustering."""
    coords = df[['latitude', 'longitude']].to_numpy()
    
    # DBSCAN automatically finds clusters based on density
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(coords)
    
    # Filter out noise points (label -1)
    unique_labels = np.unique(labels)
    valid_labels = unique_labels[unique_labels != -1]
    
    centroids = []
    cluster_sizes = []
    
    for label in valid_labels:
        cluster_points = coords[labels == label]
        centroid = np.mean(cluster_points, axis=0)
        centroids.append(centroid)
        cluster_sizes.append(len(cluster_points))
    
    print(f"DBSCAN found {len(centroids)} clusters (eps={eps}, min_samples={min_samples})")
    
    return np.array(centroids), labels, np.array(cluster_sizes)

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
    """Update earthquakes table, setting cluster_id based on cluster labels."""
    with conn.cursor() as cur:
        # Handle DBSCAN noise points (label -1) by setting cluster_id to NULL
        update_values = []
        for eq_id, label in zip(earthquake_ids, cluster_labels):
            if label == -1:  # Noise point in DBSCAN
                update_values.append((None, eq_id))
            else:
                update_values.append((cluster_ids[label], eq_id))
        
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
        print(f"Processing {len(df)} earthquake points...")

        # Choose your clustering method:
        
        # Method 1: Adaptive K-means (recommended for most cases)
        centroids, labels, cluster_sizes = run_kmeans_optimal(df, method='adaptive')
        
        # Method 2: Elbow method K-means (more scientific but slower)
        # centroids, labels, cluster_sizes = run_kmeans_optimal(df, method='elbow')
        
        # Method 3: DBSCAN (finds natural clusters but might be too many)
        # centroids, labels, cluster_sizes = run_dbscan_clustering(df, eps=2.0, min_samples=50)

        clusters_data = list(zip(centroids, cluster_sizes))

        # Store clusters in DB and get their assigned IDs
        cluster_ids = store_clusters(clusters_data, conn)

        # Update each earthquake's cluster_id
        update_earthquake_cluster_ids(conn, df['id'].tolist(), labels, cluster_ids)

        print(f"Created {len(cluster_ids)} clusters:")
        for i, size in enumerate(cluster_sizes):
            print(f"  Cluster {i+1}: {size} earthquakes")

    conn.close()