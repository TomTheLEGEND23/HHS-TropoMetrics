FROM nginx:alpine

# Copy the entire Website folder to nginx html directory
COPY frontend/Website/ /usr/share/nginx/html/

# Copy the entrypoint script
COPY frontend/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expose port 80
EXPOSE 80

# Health check: Verify nginx is serving content
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Use custom entrypoint to inject environment variables
ENTRYPOINT ["/docker-entrypoint.sh"]