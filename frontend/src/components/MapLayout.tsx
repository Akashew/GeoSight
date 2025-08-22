import { MapContainer, TileLayer } from "react-leaflet";
import { LatLngBounds } from "leaflet";
import "leaflet/dist/leaflet.css";
import EarthquakeMarkers from "./EarthquakeMarkers";
import HotspotMarkers from "./ClusterHotspots";
import "../css/MapLayout.css";
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function MapLayout() {
  const { mode: routeMode } = useParams<{ mode: "earthquakes" | "hotspots" }>();
  const navigate = useNavigate();
  const worldBounds = new LatLngBounds([-90, -180], [90, 180]);

  const [mode, setMode] = useState<"earthquakes" | "hotspots">("earthquakes");

  // Initialize mode from URL param
  useEffect(() => {
    if (routeMode === "earthquakes" || routeMode === "hotspots") {
      setMode(routeMode);
    }
  }, [routeMode]);

  const handleToggle = () => {
    const newMode = mode === "earthquakes" ? "hotspots" : "earthquakes";
    setMode(newMode);
    navigate(`/map/${newMode}`); // keep URL in sync
  };

  return (
    <div className="map-container-wrapper">
      <button className="map-toggle-btn" onClick={handleToggle}>
        Switch to {mode === "earthquakes" ? "Hotspot" : "Earthquake"} Mode
      </button>

      <MapContainer
        center={[37.7749, -122.4194]}
        zoom={2}
        scrollWheelZoom
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

        {mode === "earthquakes" ? <EarthquakeMarkers /> : <HotspotMarkers />}
      </MapContainer>
    </div>
  );
}
