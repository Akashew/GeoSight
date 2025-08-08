import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngBounds, DivIcon } from "leaflet"; // Added DivIcon import
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

  const createDiamondMarker = (magnitude: number) => {
    let magnitudeClass = "";
    if (magnitude >= 5) magnitudeClass = "magnitude-high";
    else if (magnitude >= 2) magnitudeClass = "magnitude-medium";
    else magnitudeClass = "magnitude-low";

    return new DivIcon({
      className: "custom-earthquake-marker",
      html: `<div class="diamond-marker ${magnitudeClass}"></div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12],
      popupAnchor: [0, -12],
    });
  };

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
          <Marker
            key={eq.id}
            position={[eq.latitude, eq.longitude]}
            icon={createDiamondMarker(eq.magnitude)}
          >
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
