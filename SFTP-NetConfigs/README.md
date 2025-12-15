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
├── sftp_host_key      # Private SSH host key (generated locally, mounted via K8s secret)
├── sftp_host_key.pub  # Public SSH host key (generated locally, mounted via K8s secret)
└── NetConfigs/        # Configuration files directory
    └── MLS-Test.txt   # Example Cisco MLS configuration
```

## Quick Start

### 1. Generate Static SSH Host Key

Generate the SSH key pair locally:

```bash
cd SFTP-NetConfigs
ssh-keygen -t rsa -b 4096 -f sftp_host_key -N ""
```

This creates two files:
- `sftp_host_key` (private key)
- `sftp_host_key.pub` (public key)

### 2. Create Kubernetes Secret

Create the K8s secret in the `network-services` namespace (idempotent—safe to re-run):

```bash
kubectl -n network-services create secret generic sftp-host-key \
  --from-file=ssh_host_rsa_key=sftp_host_key \
  --from-file=ssh_host_rsa_key.pub=sftp_host_key.pub \
  --dry-run=client -o yaml | kubectl apply -f -
```


### Kubernetes SFTP Server Deployment

The containerized SFTP server runs on the K3s cluster with the static SSH key mounted from the secret.

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
