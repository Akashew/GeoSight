import { useEffect, useState } from "react";
import { Marker, Popup } from "react-leaflet";
import { DivIcon } from "leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import type { EarthquakeCluster } from "../types/EarthquakeHotspot";
import { fetchClusters } from "../api/EarthquakeHotspotApi";
import "../css/ClusterHotspot.css";

export default function HotspotMarkers() {
  const [clusters, setClusters] = useState<EarthquakeCluster[]>([]);

  useEffect(() => {
    fetchClusters()
      .then(setClusters)
      .catch((err) => console.error("Failed to load clusters:", err));
  }, []);

  const getClusterSizeCategory = (size: number): string => {
    if (size < 1000) return "small";
    if (size < 3000) return "medium";
    return "large";
  };

  const calculateMarkerSize = (size: number): number => {
    // Tiered scaling approach
    if (size < 1000) {
      return Math.round(20 + (size / 1000) * 20); // 20-40px for <1000
    } else if (size < 5000) {
      return Math.round(40 + ((size - 1000) / 4000) * 30); // 40-70px for 1000-5000
    } else if (size < 10000) {
      return Math.round(70 + ((size - 5000) / 5000) * 20); // 70-90px for 5000-10000
    } else {
      return Math.round(90 + Math.min(30, ((size - 10000) / 10000) * 30)); // 90-120px for >10000
    }
  };

  const createClusterMarker = (size: number) => {
    const markerSize = calculateMarkerSize(size);
    const fontSize = Math.max(10, markerSize / 3);
    const sizeCategory = getClusterSizeCategory(size);

    return new DivIcon({
      className: "custom-cluster-marker",
      html: `<div class="cluster-marker ${sizeCategory}" style="
        width: ${markerSize}px;
        height: ${markerSize}px;
        line-height: ${markerSize}px;
        font-size: ${fontSize}px;
      ">${size.toLocaleString()}</div>`,
      iconSize: [markerSize, markerSize],
      iconAnchor: [markerSize / 2, markerSize / 2],
      popupAnchor: [0, -markerSize / 2],
    });
  };

  return (
    <MarkerClusterGroup>
      {clusters.map((cluster) => (
        <Marker
          key={cluster.id}
          position={[cluster.latitude, cluster.longitude]}
          icon={createClusterMarker(cluster.clusterSize)}
        >
          <Popup>
            <div style={{ minWidth: "200px" }}>
              <strong>Earthquake Hotspot</strong>
              <br />
              <strong>Cluster Size:</strong>{" "}
              {cluster.clusterSize.toLocaleString()} earthquakes
              <br />
              <strong>Location:</strong> {cluster.latitude.toFixed(4)}°,{" "}
              {cluster.longitude.toFixed(4)}°
              <br />
              <small>
                This hotspot contains {cluster.clusterSize} earthquake events
              </small>
            </div>
          </Popup>
        </Marker>
      ))}
    </MarkerClusterGroup>
  );
}
