#!/bin/sh
# Script to inject environment variables into JavaScript at runtime
# This runs when the container starts

set -e

echo "🔧 Configuring nginx proxy and email API..."

# Process nginx template with environment variables (if template exists)
export EMAIL_API_URL=${EMAIL_API_URL:-http://tropometrics-email-api-service:8000}
if [ -f /etc/nginx/templates/default.conf.template ]; then
    echo "📝 Processing nginx template..."
    envsubst '${EMAIL_API_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf
else
    echo "⚠️  Nginx template not found, using default configuration"
fi

# Create code directory if it doesn't exist
mkdir -p /usr/share/nginx/html/code

# Create the email config file - use relative URL (proxied by nginx)
cat > /usr/share/nginx/html/code/email-config.js <<EOF
// Auto-generated configuration from Kubernetes environment
// DO NOT EDIT - This file is generated at runtime

const EMAIL_CONFIG = {
    apiUrl: ''  // Empty string = same origin, proxied by nginx to backend
};

// Make available globally
if (typeof window !== 'undefined') {
    window.EMAIL_CONFIG = EMAIL_CONFIG;
}
EOF

echo "✅ Email API configuration injected successfully"
echo "📧 Backend API URL: ${EMAIL_API_URL}"
echo "📧 Frontend uses relative URLs (proxied by nginx)"

# Start nginx
exec nginx -g 'daemon off;'