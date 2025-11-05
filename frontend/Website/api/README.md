# TropoMetrics Weather Data API

## Overview
The TropoMetrics Weather Data API provides real-time weather information and irrigation advice for the agricultural sector. This API is served by the frontend and fetches data from Open-Meteo API.

## Endpoint

### GET /data

Returns current weather conditions, forecasts, and irrigation recommendations in JSON format.

**URL:** `http://10.0.0.101:30081/data` (Development)  
**URL:** `http://10.0.0.101:30080/data` (Production)

**Method:** `GET`

**Content-Type:** `text/html` (displays formatted JSON)

## Response Format

```json
{
  "metadata": {
    "service": "TropoMetrics Weather API",
    "version": "1.0.0",
    "timestamp": "2025-11-05T12:30:00.000Z",
    "location": {
      "latitude": -5.013,
      "longitude": -58.381,
      "timezone": "Europe/Berlin"
    },
    "source": "Open-Meteo API",
    "endpoint": "/data"
  },
  "current": {
    "temperature_celsius": 28.5,
    "temperature_fahrenheit": "83.3",
    "timestamp": "2025-11-05T12:00"
  },
  "daily": {
    "temperature_min_celsius": 22.1,
    "temperature_max_celsius": 32.4,
    "daylight_duration_seconds": 43200,
    "daylight_hours": 12,
    "daylight_minutes": 0,
    "daylight_formatted": "12h 0m"
  },
  "moisture": {
    "soil_moisture_27_to_81cm_percentage": 12.45,
    "soil_moisture_raw": 0.1245,
    "relative_humidity_percentage": 65,
    "timestamp": "2025-11-05T12:30:00.000Z"
  },
  "irrigation": {
    "advice": "Geef water",
    "advice_english": "Give water",
    "needs_water": true,
    "threshold": 0.14,
    "current_level": 0.1245
  },
  "forecast": {
    "precipitation_5day": [
      {
        "period_hours": 6,
        "precipitation_mm": 2.5,
        "date": "2025-11-05"
      }
    ],
    "total_precipitation_mm": 15.8,
    "forecast_periods": 20
  },
  "raw_data": {
    "note": "Full hourly and daily data from Open-Meteo API",
    "daily": { ... },
    "hourly_sample": {
      "precipitation_first_24h": [...],
      "relative_humidity_first_24h": [...],
      "soil_moisture_first_24h": [...]
    }
  }
}
```

## Data Fields

### Metadata
- `service`: API service name
- `version`: API version
- `timestamp`: Current server time (ISO 8601)
- `location`: Geographic coordinates and timezone
- `source`: Data source provider

### Current Weather
- `temperature_celsius`: Current temperature in Celsius
- `temperature_fahrenheit`: Current temperature in Fahrenheit
- `timestamp`: Time of measurement

### Daily Summary
- `temperature_min_celsius`: Minimum temperature for the period
- `temperature_max_celsius`: Maximum temperature for the period
- `daylight_duration_seconds`: Total daylight in seconds
- `daylight_hours`: Daylight hours (rounded)
- `daylight_minutes`: Daylight minutes
- `daylight_formatted`: Human-readable daylight duration

### Moisture Data
- `soil_moisture_27_to_81cm_percentage`: Soil moisture at 27-81cm depth (%)
- `soil_moisture_raw`: Raw soil moisture value (0-1 scale)
- `relative_humidity_percentage`: Air humidity percentage
- `timestamp`: Time of measurement

### Irrigation Advice
- `advice`: Recommendation in Dutch
- `advice_english`: Recommendation in English
- `needs_water`: Boolean indicator (true = needs watering)
- `threshold`: Moisture threshold for irrigation (0.14)
- `current_level`: Current moisture level

### Forecast
- `precipitation_5day`: Array of 6-hour precipitation periods
  - `period_hours`: Duration of the period (6)
  - `precipitation_mm`: Precipitation amount in millimeters
  - `date`: Date of the forecast period
- `total_precipitation_mm`: Total expected precipitation
- `forecast_periods`: Number of forecast periods

### Raw Data
- Complete hourly and daily data from Open-Meteo API
- First 24 hours of detailed measurements

## Usage Examples

### cURL
```bash
curl http://10.0.0.101:30081/data
```

### JavaScript/Fetch
```javascript
fetch('http://10.0.0.101:30081/data')
  .then(response => response.text())
  .then(html => {
    // Parse the JSON from the HTML page
    const jsonMatch = html.match(/<pre[^>]*>(.*?)<\/pre>/s);
    if (jsonMatch) {
      const data = JSON.parse(jsonMatch[1]);
      console.log('Current temperature:', data.current.temperature_celsius);
      console.log('Irrigation needed:', data.irrigation.needs_water);
    }
  });
```

### Python
```python
import requests
from bs4 import BeautifulSoup
import json

response = requests.get('http://10.0.0.101:30081/data')
soup = BeautifulSoup(response.text, 'html.parser')
json_data = json.loads(soup.find('pre').text)

print(f"Temperature: {json_data['current']['temperature_celsius']}°C")
print(f"Needs water: {json_data['irrigation']['needs_water']}")
```

## Notes

- Data is fetched in real-time from Open-Meteo API
- Location is currently hardcoded (latitude: -5.013, longitude: -58.381)
- Irrigation threshold: soil moisture ≤ 14% = needs water
- Forecast covers 5 days in 6-hour intervals
- All timestamps are in ISO 8601 format
- Temperature values include both Celsius and Fahrenheit

## CORS

The endpoint is accessible from any origin since it's served as a static HTML page by the frontend nginx server.

## Rate Limiting

No rate limiting is currently implemented. Usage is subject to Open-Meteo API limits.

## Support

For issues or questions about this API, contact the TropoMetrics development team.
