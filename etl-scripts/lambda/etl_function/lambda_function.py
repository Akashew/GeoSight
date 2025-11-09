import json
import requests
import pandas as pd
import pg8000.dbapi
import os
from datetime import datetime

def fetch_earthquake_data():
    """Fetch earthquake data from USGS API"""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    features = data['features']
    
    records = []
    for feature in features:
        props = feature['properties']
        geom = feature['geometry']
        record = {
            'id': feature['id'],
            'time': pd.to_datetime(props['time'], unit='ms'),
            'latitude': geom['coordinates'][1],
            'longitude': geom['coordinates'][0],
            'depth': geom['coordinates'][2],
            'magnitude': props['mag'],
            'place': props['place']
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    return df

def insert_earthquakes(df, conn):
    """Insert earthquakes into RDS"""
    insert_query = """
    INSERT INTO earthquakes (id, time, latitude, longitude, depth, magnitude, place)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE SET
        time = EXCLUDED.time,
        latitude = EXCLUDED.latitude,
        longitude = EXCLUDED.longitude,
        depth = EXCLUDED.depth,
        magnitude = EXCLUDED.magnitude,
        place = EXCLUDED.place;
    """
    
    records = list(df.itertuples(index=False, name=None))
    
    cursor = conn.cursor()
    for record in records:
        cursor.execute(insert_query, record)
    conn.commit()
    cursor.close()

def lambda_handler(event, context):
    """AWS Lambda entry point"""
    
    try:
        print("Starting ETL process...")
        start_time = datetime.now()
        
        # Fetch data from USGS
        df = fetch_earthquake_data()
        print(f"Fetched {len(df)} earthquakes from USGS")
        
        # Connect to RDS with pg8000
        conn = pg8000.dbapi.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            port=int(os.environ.get('DB_PORT', '5432'))
        )
        print("Connected to RDS")
        
        # Insert data
        insert_earthquakes(df, conn)
        print(f"Inserted/updated {len(df)} earthquakes")
        
        conn.close()
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully processed {len(df)} earthquakes',
                'earthquake_count': len(df),
                'duration_seconds': round(elapsed, 2),
                'timestamp': datetime.now().isoformat()
            })
        }
        
        print(f"ETL completed in {elapsed:.2f} seconds")
        return response
        
    except Exception as e:
        print(f"Error in ETL: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'type': type(e).__name__
            })
        }