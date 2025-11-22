# TFTP Server for Cisco Network Configurations
# Use pghalliday/tftp - a proven working TFTP Docker image
FROM pghalliday/tftp:latest

# Copy all config files from NetConfigs subfolder to /var/tftpboot
COPY NetConfigs/ /var/tftpboot/

# Set proper permissions
RUN chmod -R 755 /var/tftpboot
