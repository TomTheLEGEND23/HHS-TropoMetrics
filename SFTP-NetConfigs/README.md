### Required Extensions
https://marketplace.visualstudio.com/items?itemName=jamiewoodio.cisco

# SFTP Server for Network Device Configurations

This directory contains an SFTP server setup for serving network device configuration files, primarily for Cisco equipment.

## Directory Structure

```
SFTP-NetConfigs/
├── Dockerfile          # SFTP server container definition
├── .dockerignore       # Docker build exclusions
├── README.md          # This file (SFTP documentation)
└── NetConfigs/        # Configuration files directory
    └── MLS-Test.txt   # Example Cisco MLS configuration
```

## Quick Start

### Kubernetes SFTP Server Deployment

For easier deployment, a containerized SFTP server is available that runs on the K3s cluster.

### Access the SFTP Server

**From Cisco devices (blank device - bootstrap):**
```cisco
! Enter privileged mode
enable

! Enter global configuration
configure terminal

! Configure management interface with DHCP
interface vlan 1
 ip address dhcp
 no shutdown
 exit

! Exit configuration mode
exit

! Copy config from SFTP server
copy sftp://cisco:cisco@192.168.20.27:922/configs/MLS-Test.txt running-config
```

! Copy config from SFTP server from lab network:
```cisco
copy sftp://cisco:cisco@192.168.20.27:922/configs//MLS-Test.txt running-config
```

**From Linux client:**
```bash
# Install sftp client (usually pre-installed)
sftp -P 922 cisco:cisco@192.168.20.27
# Password: cisco
# cd configs
# get MLS-Test.txt
```

**From command line (scp):**
```bash
scp -P 922 cisco@192.168.20.27:configs/MLS-Test.txt .
# Password: cisco
```

### Router Port Forwarding

To access from external networks, forward only one port on your router:
- **External Port**: 30022 (TCP)
- **Internal IP**: 10.0.0.101
- **Internal Port**: 30022 (TCP)

### Important Notes

- **Port**: NodePort 30022 (accessible on any K3s node)
- **Security**: Encrypted and secure (SSH-based)
- **Credentials**: Username: `cisco` / Password: `cisco`
- **File Location**: `/home/cisco/configs/` inside the container
- **Image**: Uses `atmoz/sftp` (production-ready, 500M+ pulls)
- **Auto-build**: GitHub Actions builds on changes to `SFTP-NetConfigs/`

# Test connection from k3s node
ssh root@10.0.0.101
sftp -P 30022 cisco@localhost
# Password: cisco
