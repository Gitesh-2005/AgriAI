from fastapi import APIRouter, Query, HTTPException, Request
from fastapi.responses import HTMLResponse
import requests
from typing import Dict
from pydantic import BaseModel
from app.core.redis_client import redis_client
import json

OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"

router = APIRouter()


class Location(BaseModel):
    latitude: float
    longitude: float


def extract_weather_data(lat: str, lon: str) -> Dict:
    """Extract weather data from Open-Meteo API"""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "hourly": "relative_humidity_2m,precipitation_probability,rain,showers,snowfall,wind_speed_10m,wind_direction_10m"
    }
    response = requests.get(OPEN_METEO_BASE_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching weather data")
    return response.json()


def transform_weather_data(raw_data: Dict) -> Dict:
    """Transform API response into clean format"""
    if "current_weather" not in raw_data:
        raise HTTPException(status_code=500, detail="Invalid API response format")

    data = raw_data["current_weather"]
    return {
        'temperature': data.get('temperature', 0.0),
        'relative_humidity': data.get('relative_humidity', 0.0),
        'precipitation_probability': data.get('precipitation_probability', 0.0),
        'rain': data.get('rain', 0.0),
        'showers': data.get('showers', 0.0),
        'snowfall': data.get('snowfall', 0.0),
        'wind_speed': data.get('wind_speed_10m', 0.0),
        'wind_direction': data.get('wind_direction_10m', 0.0)
    }


@router.get("/", response_class=HTMLResponse)
def home():
    """Serve frontend HTML"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            button { padding: 10px 20px; font-size: 16px; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>Weather App</h1>
        <button onclick="getWeather()">Get My Weather</button>
        <pre id="output">Click the button to fetch weather...</pre>

        <script>
            async function getWeather() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(async (position) => {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        
                        const res = await fetch(`/weather?lat=${lat}&lon=${lon}`);
                        const data = await res.json();
                        document.getElementById("output").textContent = JSON.stringify(data, null, 2);
                    }, (error) => {
                        alert("Unable to fetch location: " + error.message);
                    });
                } else {
                    alert("Geolocation is not supported by this browser.");
                }
            }
        </script>
    </body>
    </html>
    """


@router.get("/weather")
def get_weather(lat: str = Query(..., description="Latitude"), lon: str = Query(..., description="Longitude")):
    """Get weather for given coordinates"""
    raw_data = extract_weather_data(lat, lon)
    transformed_data = transform_weather_data(raw_data)
    return {"location": {"latitude": lat, "longitude": lon}, "weather": transformed_data}


@router.post("/api/location")
def receive_location(loc: Location, request: Request):
    # Try to get user_id from headers, cookies, or request (customize as needed)
    user_id = request.headers.get("X-User-Id") or request.cookies.get("user_id") or "anonymous"
    print(f"Received location: {loc.latitude}, {loc.longitude} for user {user_id}")
    # Store in user context in Redis
    context_key = f"user_context:{user_id}"
    # Fetch existing context
    try:
        context_data = redis_client.get(context_key)
        context = json.loads(context_data) if context_data else {}
    except Exception:
        context = {}
    context["location"] = f"{loc.latitude},{loc.longitude}"
    redis_client.setex(context_key, 3600 * 24 * 7, json.dumps(context))
    # Fetch weather using existing logic
    raw_data = extract_weather_data(str(loc.latitude), str(loc.longitude))
    transformed_data = transform_weather_data(raw_data)
    return {"message": "Location received", "coords": loc, "weather": transformed_data}
