import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import WelcomePage from "./components/WelcomePage";
import MapLayout from "./components/MapLayout";
//import ClusterHotspots from "./components/ClusterHotspots";
import "./index.css";

const rootElement = document.getElementById("root");
if (!rootElement) throw new Error("Root element not found");

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/api/earthquakes" element={<MapLayout />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
