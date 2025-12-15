# SFTP Server for Cisco Network Configurations
# Using atmoz/sftp - production-ready SFTP server
FROM atmoz/sftp:latest

# Copy all config files from NetConfigs subfolder to cisco user directory
# Files will be accessible at /home/cisco/configs/
COPY NetConfigs/ /home/cisco/configs/

# Set proper permissions
RUN chmod -R 755 /home/cisco/configs && \
    mkdir -p /etc/ssh && \
    chmod 755 /etc/ssh

# SSH host keys will be mounted from Kubernetes secret at runtime
# Expected mounts:
#   /etc/ssh/ssh_host_ed25519_key → ed25519 private key
#   /etc/ssh/ssh_host_rsa_key → RSA private key
# Container mounts /etc/ssh as read-write to allow key generation if needed

# User will be created via command:
# cisco:cisco:1001:100:configs
# Format: username:password:uid:gid:directories
