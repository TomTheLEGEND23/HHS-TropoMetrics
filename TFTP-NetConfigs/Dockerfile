# TFTP Server for Cisco Network Configurations
# Use Alpine with tftpd-hpa for better compatibility
FROM alpine:latest

# Install tftpd-hpa
RUN apk add --no-cache tftp-hpa

# Create TFTP directory
RUN mkdir -p /var/tftpboot && \
    chmod 755 /var/tftpboot

# Copy all config files from NetConfigs subfolder to /var/tftpboot
COPY NetConfigs/ /var/tftpboot/

# Set proper permissions (world-readable for TFTP)
RUN chmod -R 755 /var/tftpboot && \
    chown -R nobody:nobody /var/tftpboot

# Expose TFTP port
EXPOSE 69/udp

# Run TFTP server with verbose logging and bind to all interfaces
# -L: standalone mode, -v: verbose, -vv: extra verbose
# --address 0.0.0.0:69 explicitly bind to all interfaces
CMD ["/usr/sbin/in.tftpd", "-L", "-vv", "--address", "0.0.0.0:69", "--secure", "--create", "/var/tftpboot"]
