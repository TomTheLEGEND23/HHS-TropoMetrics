# 🌾 TropoMetrics - Agricultural Weather Monitoring System

**Haagse Hogeschool Project**: Professional weather data service platform for the agricultural sector, built on scalable Kubernetes infrastructure with automated CI/CD.

[![Build and Deploy](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/build-deploy.yml)

## 📋 Table of Contents
- [About the Project](#about-the-project)
- [Quick Access](#quick-access)
- [Architecture](#architecture)
- [Features](#features)
- [How It Works](#how-it-works)
- [Deployment](#deployment)
  - [K3s with Portainer (Production)](#k3s-with-portainer-production)
  - [Docker Compose (Local Development)](#docker-compose-local-development)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## About the Project

**TropoMetrics** is a containerized weather monitoring platform specifically designed for agricultural applications. It provides real-time weather data, 5-day forecasts, soil moisture analysis, and irrigation recommendations to help farmers make data-driven decisions.

### What It Does
- **Real-time Weather Monitoring**: Current temperature, humidity, wind speed, and soil moisture
- **Precipitation Forecasting**: 5-day rainfall predictions with interactive charts
- **Irrigation Advice**: Automated recommendations based on weather conditions
- **Email Notifications**: Configurable weather alerts and reports
- **REST API**: Programmatic access to weather data with API key authentication
- **Mobile-Responsive UI**: Professional dashboard accessible on any device

### Technology Stack
- **Frontend**: Nginx reverse proxy serving static HTML/CSS/JavaScript
- **Backend**: FastAPI (Python 3.11) for weather data aggregation and email services
- **Weather Data**: Open-Meteo API (Amsterdam/Europe timezone)
- **Infrastructure**: K3s (Lightweight Kubernetes) on Proxmox VE
- **CI/CD**: GitHub Actions with automated image builds and deployments
- **Container Registry**: GitHub Container Registry (GHCR)
- **Orchestration**: Portainer for GitOps-based deployments

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

### System Components
```
┌──────────────────────────────────────────────────────────────┐
│                         Internet                              │
│                     (Open-Meteo API)                          │
└────────────────────────────┬─────────────────────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│              K3s Cluster (Proxmox VE)                         │
│                            │                                  │
│  ┌─────────────────────────┼─────────────────────────────┐   │
│  │    Browser → 10.0.0.101:30080 (Production)            │   │
│  │           → 10.0.0.101:30081 (Development)            │   │
│  └─────────────────────────┼─────────────────────────────┘   │
│                            │                                  │
│  ┌─────────────────────────▼─────────────────────────────┐   │
│  │  Frontend Pods (nginx:alpine)                         │   │
│  │  - Serves static HTML/CSS/JavaScript                  │   │
│  │  - Reverse proxy to backend                           │   │
│  │  - NodePort 30080/30081 (external access)             │   │
│  │  - Auto-scales: 3-12 replicas (production)            │   │
│  └─────────────────────────┬─────────────────────────────┘   │
│                            │ /api/* requests                  │
│  ┌─────────────────────────▼─────────────────────────────┐   │
│  │  Backend Pods (Python 3.11 + FastAPI)                 │   │
│  │  - Weather data aggregation & processing              │   │
│  │  - API key authentication                             │   │
│  │  - Email notification service (SMTP)                  │   │
│  │  - ClusterIP :8000 (internal only)                    │   │
│  │  - Auto-scales: 2-6 replicas (production)             │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Kubernetes Secrets (namespace: tropometrics)          │  │
│  │  - SMTP credentials (Email-Username/Password/Server)   │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline                             │
│  GitHub → Actions → Build Images → GHCR → Portainer → K3s    │
└───────────────────────────────────────────────────────────────┘
```

### Network Architecture
- **Cluster**: K3s (5 nodes) - k3s-1 (master), k3s-2 to k3s-5 (workers)
- **Network**: 10.0.0.0/24 subnet via OPNsense virtual router
- **Service Types**: 
  - Frontend: NodePort (30080 production, 30081 dev)
  - Backend: ClusterIP (internal only, port 8000)
- **DNS**: Internal Kubernetes DNS (tropometrics-backend:8000)

## Features

✅ **Real-time Weather Data**: Temperature, humidity, soil moisture, irrigation advice  
✅ **5-Day Forecast**: Precipitation predictions with interactive charts  
✅ **REST API**: JSON weather data with API key authentication  
✅ **Email Alerts**: Secure SMTP backend for weather notifications  
✅ **Responsive Design**: Mobile-friendly agricultural dashboard  
✅ **Auto-scaling**: Production scales 3-12 pods based on CPU load (40% target)  
✅ **Zero-downtime**: Rolling updates with health checks  
✅ **High Availability**: Multi-replica deployments with load balancing  
✅ **Security**: Kubernetes Secrets for sensitive data, API key auth  
✅ **GitOps**: Automated deployments via Portainer on code push

## How It Works

### Data Flow
1. **User Request**: Browser accesses dashboard at `http://10.0.0.101:30080`
2. **Frontend Serving**: Nginx serves static HTML/CSS/JavaScript
3. **API Call**: JavaScript makes authenticated request to `/api?api_key=...`
4. **Reverse Proxy**: Nginx forwards `/api/*` to backend pod at `tropometrics-backend:8000`
5. **Weather Data**: Backend fetches data from Open-Meteo API (Europe/Amsterdam timezone)
6. **Processing**: FastAPI processes, validates, and formats weather data
7. **Response**: JSON returned to frontend → JavaScript renders charts and UI
8. **Email Service**: Optional email notifications via `/api/send-email` endpoint

### Authentication & Security
- **API Keys**: Validated by backend before processing requests
- **Secrets Management**: SMTP credentials stored as Kubernetes Secrets
- **Network Isolation**: Backend only accessible within cluster (ClusterIP)
- **No Direct Backend Access**: All traffic routed through nginx reverse proxy

### Auto-scaling Behavior
- **Frontend**: 3-12 replicas based on 40% CPU utilization
- **Backend**: 2-6 replicas based on 40% CPU utilization
- **Scale Up**: 100% increase or +2 pods (whichever is greater), 1min stabilization
- **Scale Down**: 50% reduction, 5min stabilization to prevent flapping

## Deployment

### K3s with Portainer (Production)

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

### Email Notifications API

Send weather alerts via secure SMTP backend.

**Endpoint**: `POST /api/send-email`

**JavaScript Client:**
```javascript
// Using provided email-service.js
const result = await sendEmail(
    'farmer@example.com',
    'Weather Alert',
    'Heavy rain expected in the next 6 hours. Consider irrigation adjustments.'
);

if (result.success) {
    console.log('Email sent successfully:', result.message);
} else {
    console.error('Email failed:', result.error);
}
```

**Direct API Call:**
```bash
curl -X POST http://10.0.0.101:30081/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "farmer@example.com",
    "subject": "Weather Alert - Heavy Rain Expected",
    "body": "Dear Farmer,\n\nHeavy rain expected in the next 6 hours.\nConsider adjusting irrigation schedules.\n\nBest regards,\nTropoMetrics"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Email sent successfully",
  "timestamp": "2025-11-05T14:30:00Z"
}
```

**Test Page**: http://10.0.0.101:30081/email-test.html

**Rate Limits**: None currently implemented (consider adding in production)

## Configuration

### Kubernetes Secrets (Production)
Email SMTP credentials stored securely as Kubernetes secrets:

```bash
kubectl create secret generic tropometrics-email-secrets \
  --namespace=tropometrics \
  --from-literal=Email-Username=your-email@gmail.com \
  --from-literal=Email-Password=your-app-password \
  --from-literal=Email-Server=smtp.gmail.com:587
```

**View existing secrets:**
```bash
kubectl get secrets -n tropometrics
kubectl describe secret tropometrics-email-secrets -n tropometrics
```

**Update existing secret:**
```bash
kubectl delete secret tropometrics-email-secrets -n tropometrics
kubectl create secret generic tropometrics-email-secrets \
  --namespace=tropometrics \
  --from-literal=Email-Username=new-email@gmail.com \
  --from-literal=Email-Password=new-app-password \
  --from-literal=Email-Server=smtp.gmail.com:587
```

**Gmail Setup**: 
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character app password (not your regular Gmail password)

### Environment Variables (Docker Compose)
For local development, create `.env` file:

```env
# Email Service Configuration
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_SERVER=smtp.gmail.com:587

# API Keys (optional - defaults provided)
API_KEY_1=f7fdaa2c-d204-4083-9ca9-34d7bdec25ac
API_KEY_2=demo-key-12345
```

### API Keys
Valid API keys for weather data access:
- `f7fdaa2c-d204-4083-9ca9-34d7bdec25ac` (test key)
- `demo-key-12345` (demo key)

Add new keys by modifying `backend/main.py`:
```python
VALID_API_KEYS = [
    "f7fdaa2c-d204-4083-9ca9-34d7bdec25ac",
    "demo-key-12345",
    "your-new-key-here"
]
```

### Resource Limits

**Production (main-env.yaml)**:
- **Frontend**: 100m-500m CPU, 64Mi-256Mi RAM, 3-12 replicas
- **Backend**: 100m-500m CPU, 128Mi-512Mi RAM, 2-6 replicas

**Development (dev-env.yaml)**:
- **Frontend**: 50m-200m CPU, 32Mi-128Mi RAM, 1 replica
- **Backend**: 50m-200m CPU, 64Mi-256Mi RAM, 1 replica

**Adjust resources** by editing `k8s/main-env.yaml` or `k8s/dev-env.yaml`:

This is the recommended production deployment method using Portainer's GitOps capabilities.

#### Prerequisites
- K3s cluster running (v1.33+)
- Portainer installed and configured
- kubectl access to cluster
- GitHub repository with container images published to GHCR

#### Step 1: Create Namespace
```bash
kubectl create namespace tropometrics
```

#### Step 2: Configure Secrets
Create Kubernetes secret for email service:
```bash
kubectl create secret generic tropometrics-email-secrets \
  --namespace=tropometrics \
  --from-literal=Email-Username=your-email@gmail.com \
  --from-literal=Email-Password=your-app-password \
  --from-literal=Email-Server=smtp.gmail.com:587
```

**Gmail Setup**: 
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password (not your regular password)

#### Step 3: Deploy via Portainer GitOps

**Option A: Portainer UI (Recommended)**
1. Login to Portainer
2. Navigate to **Stacks** → **Add Stack**
3. Name: `tropometrics-production` or `tropometrics-dev`
4. **Build method**: Repository
5. Configure Git settings:
   - **Repository URL**: `https://github.com/TomTheLEGEND23/HHS-TropoMetrics`
   - **Repository reference**: `refs/heads/main` (production) or `refs/heads/dev`
   - **Compose path**: For production: `k8s/main-env.yaml`, For dev: `k8s/dev-env.yaml`
   - **Authentication**: None (public repo) or add GitHub token for private
6. Enable **GitOps updates** (optional - auto-redeploy on git push)
7. Click **Deploy the stack**

**Option B: Portainer API**
```bash
# Get auth token
TOKEN=$(curl -X POST http://10.0.0.101:9000/api/auth \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}' | jq -r .jwt)

# Deploy stack
curl -X POST http://10.0.0.101:9000/api/stacks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "tropometrics-production",
    "repositoryURL": "https://github.com/TomTheLEGEND23/HHS-TropoMetrics",
    "repositoryReferenceName": "refs/heads/main",
    "composeFile": "k8s/main-env.yaml",
    "type": 1,
    "endpointId": 1,
    "autoUpdate": {
      "interval": "5m"
    }
  }'
```

#### Step 4: Verify Deployment
```bash
# Check all resources
kubectl get all -n tropometrics

# Check pods are running
kubectl get pods -n tropometrics -o wide

# Check services
kubectl get svc -n tropometrics

# Check HPA (auto-scaling)
kubectl get hpa -n tropometrics

# View logs
kubectl logs -n tropometrics -l app=tropometrics-frontend-main --tail=50
kubectl logs -n tropometrics -l app=tropometrics-backend-main --tail=50
```

#### Step 5: Test Access
```bash
# Production
curl http://10.0.0.101:30080
curl http://10.0.0.101:30080/api/health

# Development
curl http://10.0.0.101:30081
curl http://10.0.0.101:30081/api/health
```

#### GitOps Workflow (Automated)
Once configured in Portainer with GitOps enabled:

1. **Developer**: Push code to `main` or `dev` branch
2. **GitHub Actions**: Automatically builds Docker images
   - Frontend: `ghcr.io/tomthelegend23/hhs-tropometrics:main|dev`
   - Backend: `ghcr.io/tomthelegend23/hhs-tropometrics-backend:main|dev`
3. **GHCR**: Stores container images
4. **Portainer**: Detects git repository changes (polls every 5min)
5. **K3s**: Pulls new images and performs rolling update
6. **Result**: Zero-downtime deployment with automatic rollback on failure

### Docker Compose (Local Development)

For local testing and development without Kubernetes.

#### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

#### Step 1: Clone Repository
```bash
git clone https://github.com/TomTheLEGEND23/HHS-TropoMetrics.git
cd HHS-TropoMetrics
```

#### Step 2: Configure Environment
Create `.env` file in project root:
```env
# Email Configuration
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_SERVER=smtp.gmail.com:587
```

#### Step 3: Build and Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

#### Step 4: Access Application
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Backend Health**: http://localhost:8000/health
- **Email Test**: http://localhost:8080/email-test.html

#### Step 5: Stop Services
```bash
# Stop containers
docker-compose down

# Remove volumes (reset state)
docker-compose down -v
```

#### Development Workflow
```bash
# Rebuild after code changes
docker-compose up --build

# Rebuild single service
docker-compose up --build frontend
docker-compose up --build backend

# View specific logs
docker-compose logs -f frontend
docker-compose logs -f backend

# Execute commands in container
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Manual Kubernetes Deployment (Without Portainer)

If you prefer kubectl directly:

```bash
# Apply manifests
kubectl apply -f k8s/main-env.yaml   # Production
kubectl apply -f k8s/dev-env.yaml    # Development

# Update deployment (after image push)
kubectl rollout restart deployment/tropometrics-frontend-main -n tropometrics
kubectl rollout restart deployment/tropometrics-backend-main -n tropometrics

# Check rollout status
kubectl rollout status deployment/tropometrics-frontend-main -n tropometrics

# Rollback if needed
kubectl rollout undo deployment/tropometrics-frontend-main -n tropometrics
```

## API Documentation
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

### Common Issues

#### Email Service Unavailable
**Symptoms**: Email health check fails, "Backend: Unavailable" shown on frontend

**Diagnosis:**
```bash
# Check backend logs
kubectl logs -n tropometrics -l app=tropometrics-backend-dev --tail=50

# Verify secret exists
kubectl get secrets -n tropometrics

# Test backend directly from frontend pod
kubectl exec -n tropometrics deployment/tropometrics-frontend-dev -- \
  wget -qO- http://tropometrics-backend:8000/health
```

**Solutions:**
1. Verify Kubernetes secret is created correctly
2. Check SMTP credentials are valid (test with Gmail)
3. Ensure backend pods are running: `kubectl get pods -n tropometrics`
4. Restart backend: `kubectl rollout restart deployment/tropometrics-backend-dev -n tropometrics`

#### Frontend 502 Bad Gateway
**Symptoms**: Nginx returns 502 when accessing `/api` endpoints

**Diagnosis:**
```bash
# Check backend service exists
kubectl get svc tropometrics-backend -n tropometrics

# Verify backend pods are ready
kubectl get pods -n tropometrics -l app=tropometrics-backend-dev

# Check nginx config
kubectl exec -n tropometrics deployment/tropometrics-frontend-dev -- cat /etc/nginx/nginx.conf
```

**Solutions:**
1. Ensure backend service name is `tropometrics-backend` (not `tropometrics-email-api-service`)
2. Verify backend is listening on port 8000
3. Check network policies allow frontend→backend communication

#### Browser Caching Issues
**Symptoms**: Old JavaScript/CSS loaded after deployment, features not working

**Solution:**
```bash
# Hard refresh in browser
# Chrome/Firefox: Ctrl + Shift + R
# Clear browser cache or open incognito window
```

**Prevention**: Version query strings already implemented (`?v=2.0`)

#### Pod Crashes / CrashLoopBackOff
**Symptoms**: Pods restart repeatedly

**Diagnosis:**
```bash
# Check pod status
kubectl get pods -n tropometrics

# View current logs
kubectl logs -n tropometrics <pod-name>

# View previous crash logs
kubectl logs -n tropometrics <pod-name> --previous

# Describe pod for events
kubectl describe pod <pod-name> -n tropometrics
```

**Common Causes:**
- Missing environment variables/secrets
- Insufficient memory/CPU limits
- Application startup errors
- Health check failures

#### Auto-scaling Not Working
**Symptoms**: Pods don't scale up under load

**Diagnosis:**
```bash
# Check HPA status
kubectl get hpa -n tropometrics

# View HPA details
kubectl describe hpa tropometrics-frontend-hpa -n tropometrics

# Check metrics server
kubectl top nodes
kubectl top pods -n tropometrics
```

**Solutions:**
1. Ensure metrics-server is installed in K3s
2. Verify CPU/memory requests are set in deployment
3. Check HPA targets and current utilization

#### Images Not Updating
**Symptoms**: New code deployed but old version still running

**Diagnosis:**
```bash
# Check current image
kubectl get deployment tropometrics-frontend-main -n tropometrics -o jsonpath='{.spec.template.spec.containers[0].image}'

# Check image pull policy
kubectl get deployment tropometrics-frontend-main -n tropometrics -o yaml | grep imagePullPolicy
```

**Solutions:**
```bash
# Force pull new image
kubectl rollout restart deployment/tropometrics-frontend-main -n tropometrics

# Verify imagePullPolicy is "Always" in manifest
# Check GitHub Actions successfully built and pushed images
```

### Useful Commands

```bash
# View all resources in namespace
kubectl get all -n tropometrics

# Watch pod status in real-time
kubectl get pods -n tropometrics -w

# Port forward to access pod directly
kubectl port-forward -n tropometrics svc/tropometrics-backend 8000:8000

# Execute shell in running pod
kubectl exec -it -n tropometrics <pod-name> -- /bin/sh

# View resource usage
kubectl top pods -n tropometrics

# Check events
kubectl get events -n tropometrics --sort-by='.lastTimestamp'

# Delete and recreate deployment
kubectl delete deployment tropometrics-frontend-main -n tropometrics
kubectl apply -f k8s/main-env.yaml
```

### Getting Help

**Check GitHub Issues**: https://github.com/TomTheLEGEND23/HHS-TropoMetrics/issues

**Review Logs**: Always start with `kubectl logs` and `kubectl describe`

**Portainer UI**: http://10.0.0.101:9000 (if accessible)

---

## License

This project is developed for educational purposes at Haagse Hogeschool.

**HHS TropoMetrics** - Agricultural weather monitoring system for precision farming.
