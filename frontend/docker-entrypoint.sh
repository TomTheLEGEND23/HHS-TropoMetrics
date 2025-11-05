#!/bin/sh
# Script to inject environment variables into JavaScript at runtime
# This runs when the container starts

set -e

echo "🔧 Configuring nginx reverse proxy and email API..."

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

echo "✅ Email API configuration injected successfully"
echo "📧 Backend service: ${EMAIL_API_URL:-tropometrics-email-api-service:8000}"
echo "📧 Frontend uses same-origin requests (proxied by nginx)"

# Start nginx
exec nginx -g 'daemon off;'