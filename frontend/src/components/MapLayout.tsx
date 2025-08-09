import { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngBounds, DivIcon } from "leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import "leaflet/dist/leaflet.css";
import "../css/MapLayout.css";

import type { Earthquake } from "../types/Earthquake";

async function fetchEarthquakeSummaries(): Promise<Earthquake[]> {
  const res = await fetch("http://localhost:8080/api/earthquakes");
  if (!res.ok) throw new Error("Failed to fetch earthquake summaries");
  return res.json();
}

async function fetchEarthquakeById(id: string): Promise<Earthquake> {
  const res = await fetch(`http://localhost:8080/api/earthquakes/${id}`);
  if (!res.ok)
    throw new Error(`Failed to fetch earthquake details for id ${id}`);
  return res.json();
}

export default function MapLayout() {
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);
  const [detailedEarthquakes, setDetailedEarthquakes] = useState<
    Record<string, Earthquake>
  >({});
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const openPopups = useRef<Set<string>>(new Set());

  const worldBounds = new LatLngBounds([-90, -180], [90, 180]);

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
    fetchEarthquakeSummaries()
      .then(setEarthquakes)
      .catch((err) => console.error("Failed to load earthquakes:", err));
  }, []);

  // Fetch details only if not cached and popup opens
  const onPopupOpen = async (id: string) => {
    openPopups.current.add(id);
    if (!detailedEarthquakes[id] && loadingId !== id) {
      setLoadingId(id);
      try {
        const data = await fetchEarthquakeById(id);
        setDetailedEarthquakes((prev) => ({ ...prev, [id]: data }));
      } catch (err) {
        console.error(err);
      } finally {
        setLoadingId(null);
      }
    }
  };

  // Remove popup from open set when closed
  const onPopupClose = (id: string) => {
    openPopups.current.delete(id);
  };

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
        {earthquakes.map((eq) => {
          const detail = detailedEarthquakes[eq.id];
          return (
            <Marker
              key={eq.id}
              position={[eq.latitude, eq.longitude]}
              icon={createDiamondMarker(eq.magnitude)}
            >
              <Popup
                eventHandlers={{
                  add: () => onPopupOpen(eq.id),
                  remove: () => onPopupClose(eq.id),
                }}
              >
                {loadingId === eq.id ? (
                  <div>Loading details...</div>
                ) : detail ? (
                  <>
                    <strong>{detail.place}</strong>
                    <br />
                    Mag: {detail.magnitude}
                    <br />
                    Depth: {detail.depth} km
                    <br />
                    Time: {new Date(detail.time).toLocaleString()}
                    <br />
                    Coordinate: {detail.latitude.toFixed(4)},{" "}
                    {detail.longitude.toFixed(4)}
                  </>
                ) : (
                  <>
                    <strong>{eq.place}</strong>
                    <br />
                    Mag: {eq.magnitude}
                    <br />
                    Time: {new Date(eq.time).toLocaleString()}
                  </>
                )}
              </Popup>
            </Marker>
          );
        })}
      </MarkerClusterGroup>
    </MapContainer>
  );
}
