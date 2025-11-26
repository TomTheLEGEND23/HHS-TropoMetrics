# SFTP Server for Cisco Network Configurations
# Using atmoz/sftp - production-ready SFTP server
FROM atmoz/sftp:latest

# Copy all config files from NetConfigs subfolder to cisco user directory
# Files will be accessible at /home/cisco/configs/
COPY NetConfigs/ /home/cisco/configs/

# Set proper permissions
RUN chmod -R 755 /home/cisco/configs

# User will be created via command:
# cisco:cisco:1001:100:configs
# Format: username:password:uid:gid:directories
