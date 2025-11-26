# SFTP Server for Network Device Configurations

This directory contains an SFTP server setup for serving network device configuration files, primarily for Cisco equipment.

## Directory Structure

```
SFTP-NetConfigs/
├── Dockerfile          # SFTP server container definition
├── docker-compose.yml  # Docker Compose configuration (if needed)
├── README.md          # This file (SFTP documentation)
└── NetConfigs/        # Configuration files directory
    └── MLS-Test.txt   # Example Cisco MLS configuration
```

## Quick Start

### Kubernetes SFTP Server Deployment

For easier deployment, a containerized SFTP server is available that runs on the K3s cluster.

### Deployment
```bash
# Deploy to K3s cluster
kubectl apply -f k8s/sftp-server.yaml

# Check status
kubectl get pods -n network-services
kubectl logs -n network-services deployment/sftp-server

# Delete deployment
kubectl delete -f k8s/sftp-server.yaml
```

### Access the SFTP Server

**From Cisco devices:**
```cisco
copy sftp://cisco@10.0.0.101:30022/configs/MLS-Test.txt running-config
# Password: cisco
```

**From Linux client:**
```bash
# Install ftp client
sudo apt install ftp

# Connect
ftp 10.0.0.101
**From Linux client:**
```bash
# Install sftp client (usually pre-installed)
sftp -P 30022 cisco@10.0.0.101
# Password: cisco
# cd configs
# get MLS-Test.txt
```

**From command line (scp):**
```bash
scp -P 30022 cisco@10.0.0.101:configs/MLS-Test.txt .
# Password: cisco
```

### Important Notes

- The SFTP server uses NodePort 30022
- Encrypted and secure (SSH-based)
- Only ONE port needed for router port forwarding
- Username: cisco / Password: cisco
- Files are in `/home/cisco/configs/` inside the container
- Server can run on any K3s node

## Why SFTP instead of TFTP/FTP

SFTP (SSH File Transfer Protocol) is superior because:
- **Encrypted** - all data is secure (vs TFTP/FTP plaintext)
- **One port only** - no passive mode complications (port 30022 only)
- **Reliable** - TCP-based like FTP but simpler
- **Easy port forwarding** - single port makes router config trivial
- **Firewall friendly** - works through NAT and firewalls easily
- **Industry standard** - widely supported on network devices
