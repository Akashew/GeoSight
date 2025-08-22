import { useNavigate } from "react-router-dom";

export default function WelcomePage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-b from-blue-200 to-blue-400">
      <h1 className="text-5xl font-bold mb-6 text-gray-800">
        Welcome to GeoSight
      </h1>
      <p className="text-lg mb-10 text-gray-700 max-w-xl text-center">
        Explore earthquake activity or discover seismic hotspots.
      </p>
      <div className="flex gap-4">
        <button
          onClick={() => navigate("/map/earthquakes")}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg shadow-lg text-lg"
        >
          Earthquake Mode
        </button>
        <button
          onClick={() => navigate("/map/hotspots")}
          className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg shadow-lg text-lg"
        >
          Hotspot Mode
        </button>
      </div>
    </div>
  );
}
