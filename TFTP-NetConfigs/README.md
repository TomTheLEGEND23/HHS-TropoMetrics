# TFTP-NetConfigs — README

## Purpose
- This folder contains the TFTP server setup for hosting Cisco network configuration files on the K3s cluster.
- The `NetConfigs/` subfolder stores all Cisco device configuration files used for the Network portion of the proof-of-concept (PoC).
- Git (GitHub) is used for version control to track changes, maintain history, and collaborate on config edits.

## Folder Structure
```
TFTP-NetConfigs/
├── Dockerfile              # TFTP server container image
├── .dockerignore          # Excludes files from Docker build
├── README.md              # This file
└── NetConfigs/            # Store all device configs here
    ├── MLS-01.txt         # Example: Multi-layer switch config
    ├── RTR-CORE-01.cfg    # Example: Core router config
    └── ...                # Add more device configs
```

## How to use
- Store one config file per device in the `NetConfigs/` subfolder with a clear filename (e.g., "MLS-01.txt").
- Commit changes to GitHub so each revision is recorded.
- Only use PoC passwords and secrets; they are for testing purposes only.
- Base config files will be created by [@TomTheLEGEND23](https://github.com/TomTheLEGEND23) in a standard structure using a script and uploaded to the repository.
- Please do NOT add any production passwords, keys, or sensitive info to these config files.
- Keep the folder structure as is for easy navigation and because it is relied upon for the TFTP server.

## Hosting a TFTP server from a Linux desktop

Clone the GitHub repository and navigate to the `TFTP-NetConfigs/NetConfigs` directory.

**Manual Install:**
Installation info from https://www.baeldung.com/linux/tftp-server-install-configure-test (accessed 22-11-2025)

- Install TFTP server:
```bash
sudo apt update
sudo apt-get install tftpd-hpa
```

- Configure TFTP server:
```bash
sudo nano /etc/default/tftpd-hpa
```

- Edit the file to contain:
```plaintext
TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/home/tom/Git/HHS-TropoMetrics/TFTP-NetConfigs/NetConfigs"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--create --secure"
```

- Verify files are world-readable:
```bash
sudo chmod -R 777 /home/tom/Git/HHS-TropoMetrics/TFTP-NetConfigs/NetConfigs
sudo chown -R nobody:nogroup /home/tom/Git/HHS-TropoMetrics/TFTP-NetConfigs/NetConfigs
```

- Start the TFTP server:
```bash
sudo systemctl start tftpd-hpa
```

- Stop the TFTP server:
```bash
sudo systemctl stop tftpd-hpa
```

- Verify TFTP server is running healthy:
```bash
sudo systemctl status tftpd-hpa.service
```

## Commands to load a config file from TFTP onto a Cisco IOS device

### Copy file into running configuration (merge)

```cisco
copy tftp: running-config
! When prompted:
! Address or name of remote host []? 10.0.0.20
! Source filename []? rtr-core-01.cfg
! Destination filename [running-config]? <press Enter>
```

Then reload the device if needed:
```cisco
reload
```
## Kubernetes TFTP Server Deployment

For easier deployment, a containerized TFTP server is available that runs on the K3s cluster.

### Deployment
```bash
# Deploy to K3s cluster
kubectl apply -f k8s/tftp-server.yaml

# Check status
kubectl get pods -n network-services
kubectl logs -n network-services deployment/tftp-server

# Delete deployment
kubectl delete -f k8s/tftp-server.yaml
```

### Access the TFTP Server

**From Cisco devices (using hostNetwork - port 69):**
```cisco
copy tftp://10.0.0.101/MLS-Test.txt running-config
```

**From Linux client:**
```bash
# Install tftp client
sudo apt install tftp-hpa

# Test connection
echo "get MLS-Test.txt" | tftp 10.0.0.101
```

### Important Notes

- The TFTP server uses `hostNetwork: true` to bind directly to the node's port 69
- This avoids Kubernetes networking issues with TFTP's dynamic port behavior
- Access is on standard port 69 (not NodePort 30069)
- Files are served from `/var/tftpboot` inside the container

## Troubleshooting TFTP Connection Issues

### Test TFTP Connection Internally (Inside Container)
```bash
# Enter the container
docker exec -it tftp-server sh

# Test from inside
tftp localhost
tftp> get MLS-Test.txt
tftp> quit
```

### Test TFTP Connection Externally
```bash
# From host machine
tftp 127.0.0.1
tftp> get MLS-Test.txt
tftp> quit

# Or one-liner
echo "get MLS-Test.txt" | tftp 127.0.0.1
```

### Common Issues and Solutions

**Issue 1: Connection refused from outside container**
- **Cause**: Port mapping doesn't work well with TFTP due to UDP and dynamic ports
- **Solution**: Use `network_mode: host` in docker-compose.yml (already configured)

**Issue 2: Permission denied**
- **Cause**: TFTP directory or files aren't readable by nobody user
- **Solution**: Check permissions:
```bash
ls -la ./NetConfigs/
# Should show: drwxr-xr-x or -rw-r--r--
```

**Issue 3: Firewall blocking UDP port 69**
- **Solution**: Allow TFTP through firewall:
```bash
# On host machine
sudo ufw allow 69/udp
# Or
sudo iptables -A INPUT -p udp --dport 69 -j ACCEPT
```

**Issue 4: SELinux blocking access**
- **Solution**: If using SELinux:
```bash
sudo setenforce 0  # Temporary - for testing only
```

### Verify TFTP Server is Running
```bash
# Check container logs
docker logs tftp-server

# Check if port 69 is listening
sudo netstat -ulnp | grep 69
# or
sudo ss -ulnp | grep 69

# Test with verbose output
tftp -v localhost
```

### Debug Mode
Enable verbose logging by adding to docker-compose.yml environment:
```yaml
environment:
  - TFTP_OPTIONS=--verbose --secure --create
```

Then check logs:
```bash
docker logs -f tftp-server
```

