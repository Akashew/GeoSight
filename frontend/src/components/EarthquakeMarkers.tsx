import { useEffect, useState, useRef } from "react";
import { Marker, Popup } from "react-leaflet";
import { DivIcon } from "leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import type { Earthquake } from "../types/Earthquake";
import { fetchEarthquakes, fetchEarthquakeById } from "../api/EarthquakeApi";
import "../css/EarthquakeMarkers.css";

export default function EarthquakeMarkers() {
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);
  const [detailedEarthquakes, setDetailedEarthquakes] = useState<
    Record<string, Earthquake>
  >({});
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const openPopups = useRef<Set<string>>(new Set());

  useEffect(() => {
    fetchEarthquakes()
      .then(setEarthquakes)
      .catch((err) => console.error("Failed to load earthquakes:", err));
  }, []);

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

  const onPopupClose = (id: string) => openPopups.current.delete(id);

  return (
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
  );
}
