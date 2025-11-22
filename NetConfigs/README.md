# NetConfigs — README

## Purpose
- This repository folder stores Cisco network configuration files used for the Network portion of the proof-of-concept (PoC).
- Git (GitHub) is used for version control to track changes, maintain history, and collaborate on config edits.

## How to use
- Keep one config file per device with a clear filename (e.g., "MLS-01.txt").
- Commit changes to GitHub so each revision is recorded.
- Only use PoC passwords and secrets; they are for testing purposes only.
- Base config files will be created by [@TomTheLEGEND23](https://github.com/TomTheLEGEND23) in a standard structure using a script and uploaded to the repository.
- Please do NOT add any production passwords, keys, or sensitive info to these config files.
- Keep the folder structure as is for easy navigation and because it is relied upon for the TFTP server.

## Hosting a TFTP server from a Linux desktop

Clone the GitHub repository and navigate to the `NetConfigs` directory.

**Install:**
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
TFTP_DIRECTORY="/home/tom/Git/HHS-TropoMetrics/NetConfigs"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--create --secure"
```

- Verify files are world-readable:
```bash
sudo chmod -R 777 /home/tom/Git/HHS-TropoMetrics/NetConfigs
sudo chown -R nobody:nogroup /home/tom/Git/HHS-TropoMetrics/NetConfigs
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

### Alternate (IOS with configure replace)

```cisco
configure replace tftp://10.0.0.20/rtr-core-01.cfg force
```

This replaces the running configuration with the file contents (check docs for your IOS version).

## Safety and Best Practices
- ✅ Do transfers over a trusted management network or VPN
- ✅ Keep sensitive information (passwords, keys) out of the Git repository for production systems
- ✅ Test config changes in a lab or maintenance window before applying to production devices
- ✅ Record which Git commit corresponds to any config pushed to hardware for traceability
- ✅ Always backup current config before applying changes:
  ```cisco
  copy running-config flash:backup-config.txt
  ```