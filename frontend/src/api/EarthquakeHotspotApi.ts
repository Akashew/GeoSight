import api from "./axios";
import type { EarthquakeCluster } from "../types/EarthquakeHotspot";

export const fetchClusters = async (): Promise<EarthquakeCluster[]> => {
  const response = await api.get<EarthquakeCluster[]>("/earthquake_clusters");
  return response.data;
};
