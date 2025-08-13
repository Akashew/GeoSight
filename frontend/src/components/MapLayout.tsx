import { MapContainer, TileLayer } from "react-leaflet";
import { LatLngBounds } from "leaflet";
import "leaflet/dist/leaflet.css";
import EarthquakeMarkers from "./EarthquakeMarkers";
import "../css/MapLayout.css";

export default function MapLayout() {
  const worldBounds = new LatLngBounds([-90, -180], [90, 180]);

  return (
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
      <EarthquakeMarkers />
    </MapContainer>
  );
}
