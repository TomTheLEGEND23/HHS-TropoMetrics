# 🌾 TropoMetrics - Professionele Weerdienst

**Haagse Hogeschool Project**: Schaalbaar, veilig en redundant netwerk met weerdata-dienst voor de agrarische sector.

Containerized weather dashboard with REST API, deployed on K3s Kubernetes cluster with automated CI/CD and multi-environment support.

[![Build and Deploy](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/build-deploy.yml)

## Quick Access

| Environment | Frontend | Weather API | Backend Health |
|------------|----------|-------------|----------------|
| **Production** | http://10.0.0.101:30080 | http://10.0.0.101:30080/api | http://10.0.0.101:30080/api/health |
| **Development** | http://10.0.0.101:30081 | http://10.0.0.101:30081/api | http://10.0.0.101:30081/api/health |

## Architecture

### Stack
- **Frontend**: Nginx + Static HTML/CSS/JavaScript
- **Backend**: FastAPI (Python 3.11) - Email & Weather API
- **Platform**: K3s (Lightweight Kubernetes) on Proxmox
- **CI/CD**: GitHub Actions → GHCR → Portainer GitOps
- **Security**: Kubernetes Secrets, API Key Authentication

### Components
```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ↓
┌─────────────────────────┐
│  Frontend (Nginx)       │  Port 30080/30081
│  - Website UI           │
│  - Reverse Proxy        │
└──────┬──────────────────┘
       │ Internal Cluster
       ↓
┌─────────────────────────┐
│  Backend (FastAPI)      │  ClusterIP :8000
│  - /api (Weather Data)  │  + API Key Auth
│  - /api/send-email      │  + Email Service
│  - /health              │
└─────────────────────────┘
```

## Features

✅ **Real-time Weather Data**: Temperature, humidity, soil moisture, irrigation advice  
✅ **5-Day Forecast**: Precipitation predictions with interactive charts  
✅ **REST API**: JSON weather data with API key authentication  
✅ **Email Alerts**: Secure SMTP backend for weather notifications  
✅ **Responsive Design**: Mobile-friendly agricultural dashboard  
✅ **Auto-scaling**: Production scales 3-12 pods based on load  
✅ **Zero-downtime**: Rolling updates with health checks

## API Endpoints

### Weather Data API
Get structured weather data with API key authentication.

```bash
# Get weather data
curl "http://10.0.0.101:30081/api?api_key=YOUR_API_KEY"
```

**Response**: JSON with current weather, forecasts, irrigation advice, and raw data.

**Valid API Keys**:
- `f7fdaa2c-d204-4083-9ca9-34d7bdec25ac` (test)
- `demo-key-12345` (demo)

See `/frontend/Website/api/README.md` for full API documentation.

### Email Notifications

Send weather alerts via secure SMTP backend.

**JavaScript:**
```javascript
const result = await sendEmail(
    'farmer@example.com',
    'Weather Alert',
    'Heavy rain expected today!'
);
```

**Direct API:**
```bash
curl -X POST http://10.0.0.101:30081/api/send-email \
  -H "Content-Type: application/json" \
  -d '{"to":"test@example.com","subject":"Alert","body":"Message"}'
```

**Test Page**: http://10.0.0.101:30081/email-test.html

## Configuration

### Kubernetes Secrets
Email SMTP credentials stored as K8s secrets:

```bash
kubectl create secret generic tropometrics-email-secrets \
  --namespace=tropometrics \
  --from-literal=Email-Username=your-email@gmail.com \
  --from-literal=Email-Password=your-app-password \
  --from-literal=Email-Server=smtp.gmail.com:587
```

**Gmail Setup**: Enable 2FA → Create App Password → https://myaccount.google.com/apppasswords

## Deployment

### K3s Cluster
**Nodes**: k3s-1 (master, 10.0.0.101), k3s-2-5 (workers, 10.0.0.102-105)  
**Namespace**: `tropometrics`  
**Management**: Portainer GitOps

### GitOps Workflow
1. Push to `main` or `dev` branch
2. GitHub Actions builds frontend + backend images
3. Pushes to GHCR (`ghcr.io/tomthelegend23/hhs-tropometrics/`)
4. Portainer auto-deploys to K3s cluster

### Manual Deployment
```bash
# Apply manifests
kubectl apply -f k8s/dev-env.yaml   # Development
kubectl apply -f k8s/main-env.yaml  # Production

# Check status
kubectl get pods,svc -n tropometrics
```

### Local Development
```bash
docker-compose up --build
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```
## Project Structure
```
├── backend/
│   ├── main.py              # FastAPI backend (weather API + email)
│   ├── requirements.txt     # httpx, fastapi, pydantic, uvicorn
│   └── Dockerfile           # Python 3.11 container
├── frontend/
│   ├── docker-entrypoint.sh # Generates email-config.js
│   ├── nginx.conf           # Reverse proxy config
│   ├── Dockerfile           # nginx:alpine container
│   └── Website/
│       ├── index.html       # Weather dashboard
│       ├── email-test.html  # Email testing page
│       ├── styles.css       # Professional styling
│       └── code/
│           ├── email-service.js   # Email API client
│           └── data-weather.js    # Weather data + charts
├── k8s/
│   ├── main-env.yaml        # Production (30080) + HPA
│   └── dev-env.yaml         # Development (30081)
├── .github/workflows/
│   └── build-deploy.yml     # CI/CD pipeline
└── docker-compose.yml       # Local development
```

## Troubleshooting

**Email unavailable:**
```bash
kubectl logs -n tropometrics -l app=tropometrics-email-api-dev
kubectl get secrets -n tropometrics
```

**Frontend 502:**
```bash
kubectl exec -n tropometrics deployment/tropometrics-dev -- \
  wget -O- http://tropometrics-email-api-service:8000/health
```

**Pod crashes:**
```bash
kubectl describe pod <pod-name> -n tropometrics
kubectl logs -n tropometrics <pod-name> --previous
```

---

**HHS TropoMetrics** - Agricultural weather monitoring system for precision farming.
