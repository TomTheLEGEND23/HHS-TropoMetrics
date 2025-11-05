#!/bin/sh
# Script to inject environment variables into JavaScript and nginx config at runtime
# This runs when the container starts

set -e

echo "🔧 Configuring nginx reverse proxy and email API..."

# Get backend service name from environment variable or use default
BACKEND_SERVICE_NAME=${BACKEND_SERVICE:-tropometrics-backend}
BACKEND_PORT=${BACKEND_PORT:-8000}

# Create code directory if it doesn't exist
mkdir -p /usr/share/nginx/html/code

# Create the email config file - empty URL means same-origin (proxied by nginx)
cat > /usr/share/nginx/html/code/email-config.js <<EOF
// Auto-generated configuration from Kubernetes environment
// DO NOT EDIT - This file is generated at runtime

const EMAIL_CONFIG = {
    apiUrl: ''  // Empty = same origin, nginx proxies to backend
};

// Make available globally
if (typeof window !== 'undefined') {
    window.EMAIL_CONFIG = EMAIL_CONFIG;
}
EOF

# Update nginx configuration with actual backend service name
sed -i "s/BACKEND_SERVICE_PLACEHOLDER/${BACKEND_SERVICE_NAME}/g" /etc/nginx/nginx.conf
sed -i "s/BACKEND_PORT_PLACEHOLDER/${BACKEND_PORT}/g" /etc/nginx/nginx.conf

echo "✅ Email API configuration injected successfully"
echo "📧 Backend service: ${BACKEND_SERVICE_NAME}:${BACKEND_PORT}"
echo "📧 Frontend uses same-origin requests (proxied by nginx)"

# Start nginx
exec nginx -g 'daemon off;'