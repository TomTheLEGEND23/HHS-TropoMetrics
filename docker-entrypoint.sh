#!/bin/sh
# Script to inject environment variables into JavaScript at runtime
# This runs when the container starts

set -e

echo "🔧 Injecting email API configuration into JavaScript..."

# Create code directory if it doesn't exist
mkdir -p /usr/share/nginx/html/code

# Create the email config file with API endpoint
cat > /usr/share/nginx/html/code/email-config.js <<EOF
// Auto-generated configuration from Kubernetes environment
// DO NOT EDIT - This file is generated at runtime

const EMAIL_CONFIG = {
    apiUrl: '${EMAIL_API_URL}'
};

// Make available globally
if (typeof window !== 'undefined') {
    window.EMAIL_CONFIG = EMAIL_CONFIG;
}
EOF

echo "✅ Email API configuration injected successfully"
echo "📧 API URL: ${EMAIL_API_URL}"

# Start nginx
exec nginx -g 'daemon off;'