# SFTP Server for Cisco Network Configurations
# Using atmoz/sftp - production-ready SFTP server
FROM atmoz/sftp:latest

# Copy all config files from NetConfigs subfolder to cisco user directory
# Files will be accessible at /home/cisco/configs/
COPY NetConfigs/ /home/cisco/configs/

# Create custom sshd_config to support legacy Cisco key exchange algorithms
RUN echo "\
Port 22\n\
Protocol 2\n\
AddressFamily any\n\
ListenAddress 0.0.0.0\n\
ListenAddress ::\n\
\n\
HostKey /etc/ssh/ssh_host_rsa_key\n\
HostKey /etc/ssh/ssh_host_ed25519_key\n\
\n\
# Support legacy algorithms for older Cisco devices\n\
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group14-sha256,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1\n\
Ciphers aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-cbc,aes192-cbc,aes256-cbc\n\
MACs hmac-sha2-256,hmac-sha2-512,hmac-sha1,umac-64@openssh.com,umac-128@openssh.com\n\
\n\
PermitRootLogin no\n\
StrictModes yes\n\
MaxAuthTries 6\n\
MaxSessions 10\n\
PubkeyAuthentication yes\n\
AuthorizedKeysFile\t.ssh/authorized_keys\n\
HostbasedAuthentication no\n\
IgnoreUserKnownHosts yes\n\
IgnoreRhosts yes\n\
PasswordAuthentication yes\n\
PermitEmptyPasswords no\n\
ChallengeResponseAuthentication no\n\
UsePAM yes\n\
X11Forwarding no\n\
PrintMotd no\n\
PrintLastLog no\n\
TCPKeepAlive yes\n\
Compression yes\n\
ClientAliveInterval 300\n\
ClientAliveCountMax 3\n\
Subsystem sftp /usr/lib/openssh/sftp-server\n\
" > /etc/ssh/sshd_config

# Set proper permissions
RUN chmod -R 755 /home/cisco/configs && \
    mkdir -p /etc/ssh && \
    chmod 755 /etc/ssh && \
    chmod 600 /etc/ssh/sshd_config

# SSH host keys will be mounted from Kubernetes secret at runtime (read-only)
# Expected mounts:
#   /etc/ssh/ssh_host_ed25519_key (read-only)
#   /etc/ssh/ssh_host_rsa_key (read-only)
# See: https://hub.docker.com/r/atmoz/sftp/ for mounting details

# User will be created via command:
# cisco:cisco:1001:100:configs
# Format: username:password:uid:gid:directories
