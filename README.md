# TropoMetrics - Leiden Weather Dashboard

Proof-of-concept project van Haagse HogeSchool voor TropoMetrics: ontwerp en implementeer een schaalbaar, veilig en redundant netwerk en een weerdata-dienst (API/webapp) met DevOps, Kubernetes, CI/CD, monitoring en ITIL-processen.

A containerized web application that displays real-time weather data for Leiden, Netherlands using the Open-Meteo API. Deployable on Kubernetes clusters via Portainer with automated CI/CD.

[![Build and Deploy to Kubernetes](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/deploy-kubernetes.yml/badge.svg)](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/deploy-kubernetes.yml)

🐳 **Container Registry**: [ghcr.io/tomthelegend23/hhs-tropometrics](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/pkgs/container/hhs-tropometrics)

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

### Automated Container Deployment
This repository includes a complete CI/CD pipeline for containerized deployment:

1. **Push to main branch** - Automatically triggers the build process
2. **GitHub Actions workflow** - Builds and pushes Docker image to GitHub Container Registry
3. **Portainer monitoring** - Automatically detects repository changes and redeploys
4. **Live application** - Available at `http://YOUR_SERVER_IP:8080` or `http://YOUR_NODE_IP:30080`

### Deployment Options

#### Option 1: Docker Compose (via Portainer Stacks)
1. In Portainer, create a new Stack
2. Connect it to this Git repository
3. Use the `docker-compose.yml` file
4. Set auto-update to monitor repository changes
5. Access via `http://YOUR_SERVER_IP:8080`

#### Option 2: Kubernetes (via kubectl or Portainer)
1. Apply the Kubernetes manifests: `kubectl apply -f k8s/deployment.yaml`
2. Access via NodePort: `http://YOUR_NODE_IP:30080`
3. For Portainer: Add as a Kubernetes application using the Git repository

#### Option 3: Manual Docker Run
```bash
docker run -d -p 8080:80 ghcr.io/tomthelegend23/hhs-tropometrics:latest
```

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
│       └── build-deploy.yml     # CI/CD pipeline for container builds
├── Website/
│   ├── index.html               # Main weather dashboard
│   └── styles.css               # Application styles
├── k8s/
│   └── deployment.yaml          # Kubernetes deployment manifests
├── .dockerignore                # Docker build exclusions
├── .gitignore                   # Git ignore rules
├── Dockerfile                   # Container build instructions
├── docker-compose.yml           # Portainer stack configuration
└── README.md                    # Project documentation
```

## Container Details

- **Base Image**: `nginx:alpine` - Lightweight and secure
- **Port**: 80 (internal), mapped to 8080 (Docker) or 30080 (Kubernetes)
- **Resources**: Minimal requirements (32Mi RAM, 50m CPU)
- **Health Checks**: Built-in HTTP health monitoring
- **Auto-restart**: Container restarts on failure

## Weather Code Mapping

The application includes comprehensive weather code descriptions for:
- Clear and cloudy conditions
- Various precipitation types (rain, drizzle, snow)
- Fog and visibility conditions
- Thunderstorms and severe weather

## Contributing

This is a proof-of-concept project for Haagse HogeSchool demonstrating weather data services with modern web technologies.
