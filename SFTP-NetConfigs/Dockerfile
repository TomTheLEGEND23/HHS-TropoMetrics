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

# SSH host key will be mounted from Kubernetes secret at runtime
# Expected mount: /run/secrets/ssh-key/ssh_host_rsa_key → /etc/ssh/ssh_host_rsa_key
# Expected mount: /run/secrets/ssh-key/ssh_host_rsa_key.pub → /etc/ssh/ssh_host_rsa_key.pub

# User will be created via command:
# cisco:cisco:1001:100:configs
# Format: username:password:uid:gid:directories
