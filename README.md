# TropoMetrics - Weather Dashboard

**Haagse Hogeschool Project**: Schaalbaar, veilig en redundant netwerk met weerdata-dienst voor de agrarische sector.

Containerized weather dashboard deployed on K3s Kubernetes cluster with automated CI/CD, GitOps, and multi-environment support.

[![Build and Deploy Container](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/actions/workflows/build-deploy.yml)

🐳 **Container Registry**: [ghcr.io/tomthelegend23/hhs-tropometrics](https://github.com/TomTheLEGEND23/HHS-TropoMetrics/pkgs/container/hhs-tropometrics)

## Architecture

- **Platform**: K3s (Lightweight Kubernetes) on Proxmox
- **Management**: Portainer with GitOps automation
- **CI/CD**: GitHub Actions with multi-branch deployments
- **Environments**: Production (main), Development (dev)
- **Container Registry**: GitHub Container Registry (GHCR)
- **Secrets Management**: Kubernetes Secrets injected as environment variables

## Features

- **Real-time Weather Data**: Current temperature, humidity, wind speed, pressure, and more
- **7-Day Forecast**: Extended weather forecast with daily high/low temperatures
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Auto-scaling**: Production environment scales 3-12 pods based on CPU usage
- **Rolling Updates**: Zero-downtime deployments with gradual rollout strategy
- **Secure Configuration**: Secrets stored in K3s, never in Git repository

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

## K3s Cluster Setup

### Infrastructure
- **k3s-1** (master): 10.0.0.101
- **k3s-2-5** (workers): 10.0.0.102-105
- **Namespace**: `tropometrics`
- **Management**: Portainer

### Environment Endpoints
| Environment | Branch | Port | URL |
|------------|--------|------|-----|
| Production | main | 30080 | http://10.0.0.101:30080 |
| Development | dev | 30081 | http://10.0.0.101:30081 |

## Deployment

### Automated GitOps Workflow

1. **Push code** to `main` or `dev` branch
2. **GitHub Actions** builds Docker image with branch-specific tag
3. **Image pushed** to GitHub Container Registry
4. **Portainer** detects repository change via GitOps
5. **Auto-deployment** pulls new image and updates pods
6. **Rolling update** ensures zero-downtime (production only)

### Initial Setup

#### 1. Create Secrets in Portainer
Navigate to: **Kubernetes → Configuration → Secrets → Add Secret**

```yaml
Name: tropometrics-email-secrets
Namespace: tropometrics
Keys:
  - Email-Username: your-smtp-username
  - Email-Password: your-smtp-password
  - Email-Server: smtp.example.com:587
```

#### 2. Deploy via Portainer GitOps
1. Open Portainer → **Applications**
2. Click **Add Application** → **Git Repository**
3. Configure:
   - **Repository URL**: `https://github.com/TomTheLEGEND23/HHS-TropoMetrics`
   - **Reference**: `refs/heads/main` (or `dev`)
   - **Manifest Path**: `k8s/main-env.yaml` (or `dev-env.yaml`)
   - **Auto-update**: Enable
4. Deploy

#### 3. Manual Deployment (Alternative)
```bash
# Production
kubectl apply -f k8s/main-env.yaml

# Development
kubectl apply -f k8s/dev-env.yaml
```

### Local Development
```bash
# Open frontend/Website/index.html in browser
# Or run with Docker:
docker build -t tropometrics ./frontend
docker run -p 8080:80 tropometrics

# Or use Docker Compose (runs both frontend and email-api):
docker-compose up
```

## Technical Stack

### Infrastructure
- **Orchestration**: K3s (Lightweight Kubernetes)
- **Container Runtime**: Docker
- **Management**: Portainer
- **CI/CD**: GitHub Actions
- **Registry**: GitHub Container Registry (GHCR)

### Application
- **Frontend**: Static HTML/CSS/JavaScript
- **Web Server**: nginx:alpine
- **API**: Open-Meteo (no key required)
- **Location**: Leiden, Netherlands (52.1601°N, 4.4970°E)

### Kubernetes Resources
- **Deployments**: Multi-environment with branch-specific images
- **Services**: NodePort exposure (30080, 30081)
- **HPA**: Auto-scaling on production (3-12 replicas, 40% CPU target)
- **Secrets**: Runtime injection via environment variables
- **Strategy**: RollingUpdate (maxUnavailable: 1, maxSurge: 2)

## Project Structure

```
├── .github/
│   ├── copilot-instructions.md     # Copilot development guidelines
│   └── workflows/
│       └── build-deploy.yml        # Multi-branch CI/CD pipeline
├── frontend/                        # Frontend service
│   ├── Website/                    # Web application files
│   │   ├── index.html              # Weather dashboard
│   │   ├── styles.css              # Responsive CSS
│   │   └── code/                   # JavaScript modules
│   │       ├── data-weather.js     # Weather data fetching
│   │       ├── email-service.js    # Email functionality
│   │       └── email-usage-example.js
│   ├── Dockerfile                  # nginx:alpine container build
│   ├── docker-entrypoint.sh        # Runtime environment injection
│   └── .dockerignore               # Frontend build exclusions
├── email-api/                       # Email API service
│   ├── main.py                     # FastAPI backend
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Python 3.11 container build
│   └── README.md                   # Email API documentation
├── k8s/                            # Kubernetes manifests
│   ├── main-env.yaml               # Production deployment + HPA
│   ├── dev-env.yaml                # Development deployment
│   └── email-api-test.yaml         # Email API test configuration
├── docker-compose.yml              # Local development orchestration
├── .dockerignore                   # Root build exclusions
├── .gitignore                      # Git exclusions
└── README.md                       # This file
```

## CI/CD Pipeline

### Trigger Events
- Push to `main` or `dev` branches
- Pull requests to these branches

### Build Process
1. Checkout code
2. Login to GHCR
3. Extract metadata (tags, labels)
4. Build Docker image with branch-specific tag
5. Push to `ghcr.io/tomthelegend23/hhs-tropometrics:{branch}`

### Image Tags
- `main` → Production image
- `dev` → Development image

## Security

- ✅ **Secrets in K3s**: Email credentials stored as Kubernetes Secrets
- ✅ **Runtime Injection**: Secrets injected into pods as environment variables
- ✅ **No Credentials in Git**: `.gitignore` prevents secret files from being committed
- ✅ **Auto-generated Config**: `docker-entrypoint.sh` creates config at container startup
- ⚠️ **Client-Side Visibility**: Current SMTP setup exposes credentials to browser (consider backend API for production)

## Monitoring & Maintenance

### View Deployment Status
```bash
kubectl get pods -n tropometrics
kubectl get hpa -n tropometrics
```

### Check Logs
```bash
kubectl logs -n tropometrics -l app=tropometrics,environment=production
```

### Update Secrets
1. Portainer → Kubernetes → Secrets → Edit `tropometrics-email-secrets`
2. Restart pods: `kubectl rollout restart deployment/tropometrics-main -n tropometrics`

### Scale Manually (override HPA)
```bash
kubectl scale deployment tropometrics-main -n tropometrics --replicas=5
```

## Resource Requirements

### Production (main)
- **Replicas**: 3-12 (auto-scaling)
- **CPU**: 100m request, 500m limit per pod
- **Memory**: 64Mi request, 256Mi limit per pod
- **Storage**: Ephemeral (stateless application)

### Development (dev)
- **Replicas**: 1 (fixed)
- **CPU**: 50m request, 200m limit
- **Memory**: 32Mi request, 128Mi limit

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name> -n tropometrics
kubectl logs <pod-name> -n tropometrics
```

### Secret issues
- Verify secret exists: `kubectl get secret tropometrics-email-secrets -n tropometrics`
- Check keys are correct: `kubectl describe secret tropometrics-email-secrets -n tropometrics`

### GitOps not auto-deploying
- Check Portainer GitOps repository settings
- Verify webhook is configured (if applicable)
- Check Portainer logs for pull errors

### Image not updating
- Confirm `imagePullPolicy: Always` in deployment YAML
- Manually restart: `kubectl rollout restart deployment/tropometrics-main -n tropometrics`

## Project Info

**Haagse Hogeschool** proof-of-concept demonstrating:
- Scalable Kubernetes deployment
- Secure secrets management
- CI/CD automation with GitOps
- Multi-environment workflows
- DevOps best practices
