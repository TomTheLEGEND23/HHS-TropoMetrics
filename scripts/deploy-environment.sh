#!/bin/bash
# Multi-environment deployment script for TropoMetrics
# Usage: ./deploy-environment.sh [main|dev|test|all] [deploy|delete|status]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENTS=("main" "dev" "test")
PORTS=("30080" "30081" "30082")
NAMESPACES=("tropometrics-main" "tropometrics-dev" "tropometrics-test")

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
}

deploy_environment() {
    local env=$1
    local manifest="k8s/portainer-${env}.yaml"
    
    if [ ! -f "$manifest" ]; then
        log_error "Manifest file $manifest not found"
        return 1
    fi
    
    log_info "Deploying $env environment..."
    kubectl apply -f "$manifest"
    
    # Wait for deployment to be ready
    local namespace="tropometrics-${env}"
    if [ "$env" = "main" ]; then
        namespace="tropometrics-main"
    fi
    
    log_info "Waiting for deployment to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/tropometrics -n "$namespace"
    
    # Get node IP and port
    local port
    case $env in
        main) port="30080" ;;
        dev) port="30081" ;;
        test) port="30082" ;;
    esac
    
    local node_ip=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
    
    log_info "✅ $env environment deployed successfully!"
    log_info "🌐 Access URL: http://$node_ip:$port"
}

delete_environment() {
    local env=$1
    local manifest="k8s/portainer-${env}.yaml"
    
    if [ ! -f "$manifest" ]; then
        log_error "Manifest file $manifest not found"
        return 1
    fi
    
    log_warn "Deleting $env environment..."
    kubectl delete -f "$manifest" --ignore-not-found=true
    log_info "✅ $env environment deleted"
}

show_status() {
    local env=$1
    local namespace="tropometrics-${env}"
    if [ "$env" = "main" ]; then
        namespace="tropometrics-main"
    fi
    
    echo ""
    log_header "$env Environment Status"
    
    echo "📦 Namespace:"
    kubectl get namespace "$namespace" 2>/dev/null || echo "❌ Namespace not found"
    
    echo ""
    echo "🚀 Deployment:"
    kubectl get deployment -n "$namespace" 2>/dev/null || echo "❌ No deployment found"
    
    echo ""
    echo "📋 Pods:"
    kubectl get pods -n "$namespace" 2>/dev/null || echo "❌ No pods found"
    
    echo ""
    echo "🌐 Service:"
    kubectl get svc -n "$namespace" 2>/dev/null || echo "❌ No service found"
    
    # Show access URL
    local port
    case $env in
        main) port="30080" ;;
        dev) port="30081" ;;
        test) port="30082" ;;
    esac
    
    local node_ip=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}' 2>/dev/null)
    if [ ! -z "$node_ip" ]; then
        echo ""
        echo "📍 Access URL: http://$node_ip:$port"
    fi
}

show_all_status() {
    log_header "TropoMetrics Multi-Environment Status"
    
    echo "🏠 Cluster Nodes:"
    kubectl get nodes -o wide
    echo ""
    
    for env in "${ENVIRONMENTS[@]}"; do
        show_status "$env"
    done
    
    echo ""
    log_header "Quick Access URLs"
    local node_ip=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}' 2>/dev/null)
    if [ ! -z "$node_ip" ]; then
        echo "🏭 Production (main): http://$node_ip:30080"
        echo "🔧 Development (dev): http://$node_ip:30081"
        echo "🧪 Testing (test):    http://$node_ip:30082"
    fi
}

show_help() {
    echo "TropoMetrics Multi-Environment Deployment Script"
    echo ""
    echo "Usage: $0 [ENVIRONMENT] [ACTION]"
    echo ""
    echo "Environments:"
    echo "  main    Production environment (port 30080)"
    echo "  dev     Development environment (port 30081)"
    echo "  test    Testing environment (port 30082)"
    echo "  all     All environments"
    echo ""
    echo "Actions:"
    echo "  deploy  Deploy the environment(s)"
    echo "  delete  Delete the environment(s)"
    echo "  status  Show status of environment(s)"
    echo ""
    echo "Examples:"
    echo "  $0 dev deploy     # Deploy development environment"
    echo "  $0 all status     # Show status of all environments"
    echo "  $0 test delete    # Delete testing environment"
    echo "  $0 main deploy    # Deploy production environment"
}

# Main script logic
ENVIRONMENT=${1:-"help"}
ACTION=${2:-"status"}

check_kubectl

case "$ENVIRONMENT" in
    "main"|"dev"|"test")
        case "$ACTION" in
            "deploy")
                deploy_environment "$ENVIRONMENT"
                ;;
            "delete")
                delete_environment "$ENVIRONMENT"
                ;;
            "status")
                show_status "$ENVIRONMENT"
                ;;
            *)
                log_error "Invalid action: $ACTION"
                show_help
                exit 1
                ;;
        esac
        ;;
    "all")
        case "$ACTION" in
            "deploy")
                for env in "${ENVIRONMENTS[@]}"; do
                    deploy_environment "$env"
                done
                ;;
            "delete")
                for env in "${ENVIRONMENTS[@]}"; do
                    delete_environment "$env"
                done
                ;;
            "status")
                show_all_status
                ;;
            *)
                log_error "Invalid action: $ACTION"
                show_help
                exit 1
                ;;
        esac
        ;;
    "help"|*)
        show_help
        ;;
esac