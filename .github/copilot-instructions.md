# Environment

Proxmox server running K3s (lightweight Kubernetes) cluster.

## K3s Cluster Nodes
- k3s-1 (master) - 10.0.0.101
- k3s-2 (worker) - 10.0.0.102
- k3s-3 (worker) - 10.0.0.103
- k3s-4 (worker) - 10.0.0.104
- k3s-5 (worker) - 10.0.0.105

## Infrastructure

### Hosting Platform
- **Virtualization**: Proxmox VE
- **Orchestration**: K3s (Lightweight Kubernetes)
- **Container Runtime**: Docker
- **Management UI**: Portainer
- **Network**: 10.0.0.0/24 subnet (virtual OPNsense router on Proxmox vmbr1)
- **Service Access**: 10.0.0.101 (master node) via NodePort

### Kubernetes Configuration
- **Namespace**: tropometrics (use ONLY this namespace)
- **Service Type**: NodePort (30080-30081)
- **Image Registry**: GitHub Container Registry (ghcr.io)
- **Image Pull Policy**: Always (ensures latest images)
- **Deployment Strategy**: RollingUpdate (maxUnavailable: 1, maxSurge: 2)

### Application Stack
- **Web Server**: nginx:alpine
- **Frontend**: Static HTML/CSS/JavaScript
- **API**: Open-Meteo (external, no authentication)
- **Secrets**: Kubernetes Secrets → env vars → runtime injection

### CI/CD Pipeline
- **Platform**: GitHub Actions
- **Trigger**: Push to main/dev branches
- **Build**: Docker multi-stage build
- **Registry**: ghcr.io/tomthelegend23/hhs-tropometrics
- **Deployment**: GitOps via Portainer (auto-pull on repo change)

### Resource Allocation

#### Production (main branch)
- **Replicas**: 3-12 (HorizontalPodAutoscaler)
- **CPU**: 100m request, 500m limit per pod
- **Memory**: 64Mi request, 256Mi limit per pod
- **Scaling Trigger**: 40% CPU utilization

#### Development (dev branch)
- **Replicas**: 1 (fixed)
- **CPU**: 50m request, 200m limit
- **Memory**: 32Mi request, 128Mi limit

## Development Guidelines
- Do NOT create additional namespaces - use namespace "tropometrics"
- Do NOT create unused resources
- Do NOT create unnecessary Makefiles
- Do NOT create markdown files for documentation or progress tracking
- Secrets MUST be stored in K3s secrets and injected as environment variables
- Secrets MUST NOT be stored in Git repository
- Update README.md with deployment instructions and technical details after changes
- If any information about the infrastructure added/changed, update copilot-instructions.md accordingly
- Scan codebase for unused code/files and report findings to user for confirmation before removal
- do not add security vulnerabilities and warn the user is there are any
- use the branch name when creating new resources or labels for a services in that branch

## Environment Endpoints
| Environment | Branch | Port | URL |
|------------|--------|------|-----|
| Production | main | 30080 | http://10.0.0.101:30080 |
| Development | dev | 30081 | http://10.0.0.101:30081 |

## Code Structure
- **Frontend**: Website/index.html, Website/styles.css, Website/code/email-service.js
- **Frontend Container**: Dockerfile (nginx:alpine base)
- **Email API**: email-api/main.py (FastAPI backend)
- **Email API Container**: email-api/Dockerfile (Python 3.11)
- **Entrypoint**: docker-entrypoint.sh (API URL injection)
- **Manifests**: k8s/main-env.yaml, k8s/dev-env.yaml (both include email-api deployment)
- **CI/CD**: .github/workflows/build-deploy.yml (builds both images)
- **Secrets**: Stored in K8s, accessed only by email-api backend