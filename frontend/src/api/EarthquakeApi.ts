import api from "./axios";
import type { Earthquake } from "../types/Earthquake";

export const fetchEarthquakes = async (): Promise<Earthquake[]> => {
  const response = await api.get<Earthquake[]>("/earthquakes");
  return response.data;
};

export const fetchEarthquakeById = async (id: string): Promise<Earthquake> => {
  const response = await api.get<Earthquake>(`/earthquakes/${id}`);
  return response.data;
};
