# TropoMetrics - Leiden Weather Dashboard

Proof-of-concept project van Haagse HogeSchool voor TropoMetrics: ontwerp en implementeer een schaalbaar, veilig en redundant netwerk en een weerdata-dienst (API/webapp) met DevOps, Kubernetes, CI/CD, monitoring en ITIL-processen.

A static web application that displays real-time weather data for Leiden, Netherlands using the Open-Meteo API.

[![Deploy to GitHub Pages](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/deploy.yml/badge.svg)](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/deploy.yml)

🌐 **Live Site**: [https://TomTheLEGEND23.github.io/HHS-TropoMetrics](https://TomTheLEGEND23.github.io/HHS-TropoMetrics)

## Features

- **Real-time Weather Data**: Current temperature, humidity, wind speed, pressure, and more
- **7-Day Forecast**: Extended weather forecast with daily high/low temperatures
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Auto-refresh**: Updates data every 10 minutes automatically
- **GitHub Pages Ready**: Static HTML page optimized for GitHub Pages deployment

## Weather Data Includes

### Current Weather
- Temperature and "feels like" temperature
- Weather conditions with descriptive codes
- Wind speed and direction
- Humidity and atmospheric pressure
- UV index and visibility
- Cloud cover and precipitation

### 7-Day Forecast
- Daily high and low temperatures
- Weather conditions for each day
- Date and day of the week

## API Source

This application uses the [Open-Meteo API](https://open-meteo.com/en/features#available_apis), which provides:
- Free weather data access
- No API key required
- High-quality meteorological data
- Multiple forecast models
- Global coverage

## Deployment

### Automatic GitHub Pages Deployment
This repository includes a simple CI/CD pipeline using GitHub Actions:

1. **Push to main branch** - Automatically triggers deployment
2. **GitHub Actions workflow** - Deploys the site to GitHub Pages
3. **Live site** - Available at `https://TomTheLEGEND23.github.io/HHS-TropoMetrics`

The deployment workflow:
- Checks out the repository code
- Configures GitHub Pages
- Uploads the entire repository as an artifact
- Deploys to GitHub Pages

### Manual Deployment
1. Go to your repository Settings → Pages
2. Select source: "GitHub Actions"
3. The site will automatically deploy on the next push to main

### Local Development
Simply open `index.html` in any modern web browser. The weather data will be fetched directly from the Open-Meteo API.

## Technical Details

- **Location**: Leiden, Netherlands (52.1601°N, 4.4970°E)
- **Timezone**: Europe/Amsterdam
- **Update Frequency**: Every 10 minutes
- **Browser Compatibility**: Modern browsers with ES6+ support
- **Responsive Breakpoint**: 768px for mobile optimization

## Project Structure

```
├── .github/
│   └── workflows/
│       └── deploy.yml     # Simple CI/CD deployment pipeline
├── .gitignore            # Git ignore rules
├── index.html           # Main weather dashboard (fetches APIs directly)
└── README.md           # Project documentation
```

## Weather Code Mapping

The application includes comprehensive weather code descriptions for:
- Clear and cloudy conditions
- Various precipitation types (rain, drizzle, snow)
- Fog and visibility conditions
- Thunderstorms and severe weather

## Contributing

This is a proof-of-concept project for Haagse HogeSchool demonstrating weather data services with modern web technologies.
