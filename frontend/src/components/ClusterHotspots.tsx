import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { DivIcon } from "leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import "leaflet/dist/leaflet.css";

type EarthquakeCluster = {
  id: number;
  latitude: number;
  longitude: number;
  clusterSize: number;
};

async function fetchClusters(): Promise<EarthquakeCluster[]> {
  const res = await fetch("http://localhost:8080/api/earthquake_clusters");
  if (!res.ok) throw new Error("Failed to fetch earthquake clusters");
  return res.json();
}

export default function ClusterHotspotPage() {
  const [clusters, setClusters] = useState<EarthquakeCluster[]>([]);

  // Custom marker icon for clusters (e.g. circle with size scaled by clusterSize)
  const createClusterMarker = (size: number) => {
    return new DivIcon({
      className: "custom-cluster-marker",
      html: `<div style="
        background: rgba(255, 0, 0, 0.6);
        border-radius: 50%;
        width: ${20 + size * 3}px;
        height: ${20 + size * 3}px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        border: 2px solid darkred;
      ">${size}</div>`,
      iconSize: [20 + size * 3, 20 + size * 3],
      iconAnchor: [(20 + size * 3) / 2, (20 + size * 3) / 2],
      popupAnchor: [0, -((20 + size * 3) / 2)],
    });
  };

  useEffect(() => {
    fetchClusters()
      .then(setClusters)
      .catch((err) => console.error("Failed to load clusters:", err));
  }, []);

  return (
    <MapContainer
      center={[37.7749, -122.4194]}
      zoom={2}
      scrollWheelZoom={true}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <MarkerClusterGroup>
        {clusters.map((cluster) => (
          <Marker
            key={cluster.id}
            position={[cluster.latitude, cluster.longitude]}
            icon={createClusterMarker(cluster.clusterSize)}
          >
            <Popup>
              <div>
                <strong>Cluster ID: {cluster.id}</strong>
                <br />
                Size: {cluster.clusterSize}
                <br />
                Lat: {cluster.latitude.toFixed(4)}
                <br />
                Lon: {cluster.longitude.toFixed(4)}
              </div>
            </Popup>
          </Marker>
        ))}
      </MarkerClusterGroup>
    </MapContainer>
  );
}
