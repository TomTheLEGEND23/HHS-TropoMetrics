# TFTP Server for Cisco Network Configurations
FROM alpine:latest

# Install TFTP server
RUN apk add --no-cache tftp-hpa

# Create TFTP directory
RUN mkdir -p /Configs

# Copy all config files from NetConfigs subfolder
COPY NetConfigs/ /Configs/

# Set proper permissions for TFTP
RUN chmod -R 755 /Configs && \
    chown -R nobody:nogroup /Configs

# Expose TFTP port
EXPOSE 69/udp

# Health check (check if process is running)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pgrep in.tftpd || exit 1

# Start TFTP server
# -L: Run standalone (not from inetd)
# -s: Secure mode (chroot to directory)
# -c: Allow new files to be created
# -v: Verbose logging
CMD ["/usr/sbin/in.tftpd", "-L", "-s", "/Configs", "-c", "-v"]
