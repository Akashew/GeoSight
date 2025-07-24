import requests
import pandas as pd

def fetch_earthquake_data():
    #past 30 days, all magnitudes, geojson format
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    
    response = requests.get(url)
    response.raise_for_status()  # raise error if request failed
    
    data = response.json()
    
    # Extract features list from the geojson response
    features = data['features']
    
    # Parse features into a list of dicts
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

if __name__ == "__main__":
    df = fetch_earthquake_data()
    print(df.head())


