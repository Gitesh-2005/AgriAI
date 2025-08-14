import React, { useState } from "react";

const LocationFetcher: React.FC = () => {
  const [status, setStatus] = useState<string>("");
  const [coords, setCoords] = useState<{ lat: number; lon: number } | null>(null);
  const [weather, setWeather] = useState<any>(null);

  const getLocation = () => {
    if (!navigator.geolocation) {
      setStatus("Geolocation is not supported by your browser.");
      return;
    }

    setStatus("Locating…");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        setCoords({ lat: latitude, lon: longitude });
        setStatus("Location found!");

        // Fetch weather from backend
        fetch(`/weather/weather?lat=${latitude}&lon=${longitude}`)
          .then((res) => {
            if (!res.ok) throw new Error("Failed to fetch weather");
            return res.json();
          })
          .then((data) => {
            setWeather(data.weather);
          })
          .catch((err) => {
            setStatus("Error fetching weather: " + err.message);
          });
      },
      (error) => {
        setStatus(`Error: ${error.message}`);
      }
    );
  };

  return (
    <div>
      <button
        onClick={getLocation}
        style={{
          padding: "10px 20px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Get My Location & Weather
      </button>
      <p>{status}</p>
      {coords && (
        <p>
          Latitude: {coords.lat}, Longitude: {coords.lon}
        </p>
      )}
      {weather && (
        <pre style={{ background: '#f4f4f4', padding: 10, borderRadius: 8 }}>
          {JSON.stringify(weather, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default LocationFetcher;
