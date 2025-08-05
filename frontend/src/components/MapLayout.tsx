import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngBounds } from "leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import "leaflet/dist/leaflet.css";
import "../css/MapLayout.css";

import { fetchEarthquakes } from "../api/EarthquakeApi";
import type { Earthquake } from "../types/Earthquake";

export default function MapLayout() {
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);

  const worldBounds = new LatLngBounds(
    [-90, -180], // Southwest corner
    [90, 180] // Northeast corner
  );

  useEffect(() => {
    fetchEarthquakes()
      .then(setEarthquakes)
      .catch((err) => console.error("Failed to load earthquakes:", err));
  }, []);

  return (
    <MapContainer
      center={[37.7749, -122.4194]}
      zoom={4}
      scrollWheelZoom={true}
      className="map-container"
      minZoom={2}
      maxZoom={10}
      worldCopyJump={false}
      maxBounds={worldBounds}
      maxBoundsViscosity={1.0}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <MarkerClusterGroup>
        {earthquakes.map((eq) => (
          <Marker key={eq.id} position={[eq.latitude, eq.longitude]}>
            <Popup>
              <strong>{eq.place}</strong>
              <br />
              Mag: {eq.magnitude} <br />
              Depth: {eq.depth} km
              <br />
              Time: {new Date(eq.time).toLocaleString()}
            </Popup>
          </Marker>
        ))}
      </MarkerClusterGroup>
    </MapContainer>
  );
}
