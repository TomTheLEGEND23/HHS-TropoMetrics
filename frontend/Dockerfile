FROM nginx:alpine

# Copy the entire Website folder to nginx html directory
COPY Website/ /usr/share/nginx/html/

# Copy the entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copy custom nginx configuration if needed
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Health check: Verify nginx is serving content AND email backend is accessible via K8s DNS
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ && \
        wget --no-verbose --tries=1 --spider http://tropometrics-email-api-service:8000/health || exit 1

# Use custom entrypoint to inject environment variables
ENTRYPOINT ["/docker-entrypoint.sh"]