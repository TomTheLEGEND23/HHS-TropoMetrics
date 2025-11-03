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

# Use custom entrypoint to inject environment variables
ENTRYPOINT ["/docker-entrypoint.sh"]