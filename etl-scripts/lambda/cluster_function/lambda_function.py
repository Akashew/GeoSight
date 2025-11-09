import json
import pg8000.dbapi
import os
import numpy as np
from datetime import datetime
from sklearn.cluster import KMeans

def fetch_earthquake_data(conn):
    """Fetch earthquake coordinates from RDS"""
    query = """
    SELECT id, latitude, longitude 
    FROM earthquakes
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
    """
    
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    
    return rows

def run_kmeans_clustering(coords, n_clusters=None):
    """Run K-means clustering with adaptive cluster count"""
    n_points = len(coords)
    
    if n_clusters is None:
        # Adaptive cluster count based on data size
        if n_points < 1000:
            n_clusters = max(3, n_points // 100)
        elif n_points < 5000:
            n_clusters = max(8, n_points // 300)
        elif n_points < 15000:
            n_clusters = max(15, n_points // 500)
        else:
            n_clusters = max(20, min(50, n_points // 800))
    
    print(f"Using {n_clusters} clusters for {n_points} earthquakes")
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(coords)
    centroids = kmeans.cluster_centers_
    
    cluster_sizes = np.bincount(labels)
    
    return centroids, labels, cluster_sizes

def store_clusters(clusters, conn):
    """Insert clusters into earthquake_clusters table"""
    with conn.cursor() as cur:
        # Clear existing clusters
        cur.execute("DELETE FROM earthquake_clusters;")
        
        # Insert new clusters
        insert_query = """
        INSERT INTO earthquake_clusters (latitude, longitude, cluster_size)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        
        cluster_ids = []
        for (lat, lon), size in clusters:
            cur.execute(insert_query, (float(lat), float(lon), int(size)))
            cluster_id = cur.fetchone()[0]
            cluster_ids.append(cluster_id)
        
        conn.commit()
    
    return cluster_ids

def update_earthquake_clusters(conn, earthquake_ids, labels, cluster_ids):
    """Update earthquakes with their cluster_id"""
    with conn.cursor() as cur:
        update_query = """
        UPDATE earthquakes 
        SET cluster_id = %s 
        WHERE id = %s;
        """
        
        updates = [(cluster_ids[label], eq_id) for eq_id, label in zip(earthquake_ids, labels)]
        cur.executemany(update_query, updates)
        conn.commit()

def lambda_handler(event, context):
    """AWS Lambda entry point"""
    
    try:
        print("Starting clustering process...")
        start_time = datetime.now()
        
        # Connect to RDS
        conn = pg8000.dbapi.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            port=int(os.environ.get('DB_PORT', '5432'))
        )
        print("Connected to RDS")
        
        # Fetch earthquake data
        rows = fetch_earthquake_data(conn)
        print(f"Fetched {len(rows)} earthquakes")
        
        if len(rows) == 0:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No earthquakes to cluster'})
            }
        
        # Extract data
        earthquake_ids = [row[0] for row in rows]
        coords = np.array([[row[1], row[2]] for row in rows])
        
        # Run clustering
        centroids, labels, cluster_sizes = run_kmeans_clustering(coords)
        print(f"Created {len(centroids)} clusters")
        
        # Store clusters
        clusters_data = list(zip(centroids, cluster_sizes))
        cluster_ids = store_clusters(clusters_data, conn)
        print("Stored clusters in database")
        
        # Update earthquakes with cluster assignments
        update_earthquake_clusters(conn, earthquake_ids, labels, cluster_ids)
        print("Updated earthquake cluster assignments")
        
        conn.close()
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # Summary
        cluster_summary = [
            {'cluster_id': i+1, 'size': int(size)} 
            for i, size in enumerate(cluster_sizes)
        ]
        
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully clustered {len(rows)} earthquakes',
                'cluster_count': len(centroids),
                'earthquake_count': len(rows),
                'clusters': cluster_summary[:10],
                'duration_seconds': round(elapsed, 2),
                'timestamp': datetime.now().isoformat()
            })
        }
        
        print(f"Clustering completed in {elapsed:.2f} seconds")
        return response
        
    except Exception as e:
        print(f"Error in clustering: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'type': type(e).__name__
            })
        }