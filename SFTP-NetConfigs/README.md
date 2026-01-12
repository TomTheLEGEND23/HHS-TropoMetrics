# Network Topology

This document provides an overview of the network topology designed for the project. The topology is represented in the Draw.io diagram located in the same directory.

## Diagrams
### PoC Design Diagram
- **Diagram Name**: PoC-ontwerp
- **Description**: This diagram represents the Proof of Concept design.



### Required Extensions
https://marketplace.visualstudio.com/items?itemName=jamiewoodio.cisco

# SFTP Server for Network Device Configurations

This directory contains an SFTP server setup for serving network device configuration files, primarily for Cisco equipment.

## Directory Structure

```
SFTP-NetConfigs/
├── Dockerfile          # SFTP server container definition (includes legacy algorithm support)
├── .dockerignore       # Docker build exclusions
├── README.md          # This file (SFTP documentation)
├── sftp_host_ed25519_key      # ed25519 private SSH host key (generated locally, mounted via K8s secret)
├── sftp_host_ed25519_key.pub  # ed25519 public SSH host key
├── sftp_host_rsa_key          # RSA private SSH host key (generated locally, mounted via K8s secret)
├── sftp_host_rsa_key.pub      # RSA public SSH host key
└── NetConfigs/        # Configuration files directory
    └── MLS-Test.txt   # Example Cisco MLS configuration
```

## Quick Start

### Kubernetes SFTP Server Deployment

The containerized SFTP server runs on the K3s cluster with the static SSH key mounted from the secret.

### Access the SFTP Server

**From Cisco devices (blank device - bootstrap):**
Switch Setup with VLAN1:
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
```

Switch Setup with GigabitEthernet0/0:
```cisco
! Enter privileged mode
enable
! Enter global configuration
configure terminal
! Configure management interface with DHCP
interface GigabitEthernet0/0
 ip address dhcp
 no shutdown
 exit
! Exit configuration mode
exit
```

Router Setup:
```cisco
! Enter privileged mode
enable
! Enter global configuration
configure terminal
! Configure management interface with DHCP
interface GigabitEthernet0/0/0
 ip address dhcp
 no shutdown
 exit
! Exit configuration mode
exit
```

After Waiting a few moments for DHCP to assign an IP address, verify the assigned IP:
```cisco
! Copy config from SFTP server
copy scp://cisco@192.168.20.27/configs/XXX.ios running-config
```

**From Linux client:**
```bash
# Install sftp client (usually pre-installed)
sftp cisco:cisco@192.168.20.27
# Password: cisco
# cd configs
# get MLS-Test.txt
```

**From command line (scp):**
```bash
scp cisco@192.168.20.27:configs/MLS-Test.txt .
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
- **Legacy Algorithms**: Dockerfile includes support for older Cisco devices (diffie-hellman-group1-sha1, etc.)
- **Auto-build**: GitHub Actions builds on changes to `SFTP-NetConfigs/`

# Test connection from k3s node
ssh root@10.0.0.101
sftp -P 30022 cisco@localhost
# Password: cisco
