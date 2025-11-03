#!/bin/sh
# Script to inject environment variables into JavaScript at runtime
# This runs when the container starts

set -e

echo "🔧 Injecting SMTP email configuration into JavaScript..."

# Create code directory if it doesn't exist
mkdir -p /usr/share/nginx/html/code

# Create the email config file from environment variables
cat > /usr/share/nginx/html/code/email-config.js <<EOF
// Auto-generated configuration from Kubernetes secrets
// DO NOT EDIT - This file is generated at runtime

const EMAIL_CONFIG = {
    username: '${EMAIL_USERNAME}',
    password: '${EMAIL_PASSWORD}',
    server: '${EMAIL_SERVER}'
};

// Make available globally
if (typeof window !== 'undefined') {
    window.EMAIL_CONFIG = EMAIL_CONFIG;
}
EOF

echo "✅ Email configuration injected successfully"
echo "📧 Server: ${EMAIL_SERVER}"
echo "📧 Username: ${EMAIL_USERNAME}"

# Start nginx
exec nginx -g 'daemon off;'