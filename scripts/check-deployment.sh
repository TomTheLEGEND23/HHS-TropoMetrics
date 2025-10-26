#!/bin/bash
# Script to check TropoMetrics deployment status in k3s dev environment
# Save as check-deployment.sh and run: chmod +x check-deployment.sh && ./check-deployment.sh

echo "🔍 Checking TropoMetrics Deployment Status..."
echo "============================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

echo "🎯 TropoMetrics Namespace:"
kubectl get namespace tropometrics 2>/dev/null || echo "❌ TropoMetrics namespace not found"

echo ""
echo "🚀 Deployment Status:"
kubectl get deployment -n tropometrics 2>/dev/null || echo "❌ No deployments found"

echo ""
echo "📦 Pod Status:"
kubectl get pods -n tropometrics 2>/dev/null || echo "❌ No pods found"

echo ""
echo "🌐 Service Information:"
kubectl get svc -n tropometrics 2>/dev/null || echo "❌ No services found"

echo ""
echo "🏠 Node Information:"
kubectl get nodes -o wide

echo ""
echo "📡 Access Your Application:"
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
if [ ! -z "$NODE_IP" ]; then
    echo "🌤️  TropoMetrics Weather Dashboard: http://$NODE_IP:30080"
else
    echo "❌ Could not determine node IP"
fi

echo ""
echo "🔧 Useful Commands:"
echo "  View logs: kubectl logs -n tropometrics -l app=tropometrics"
echo "  Restart:   kubectl rollout restart deployment/tropometrics -n tropometrics"
echo "  Delete:    kubectl delete namespace tropometrics"