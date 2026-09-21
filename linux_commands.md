# Linux Commands Used

These commands were used during the Linux VM lab for basic system validation and generation of workload activity.

```bash
# Update package list
sudo apt update

# Install stress utility to generate CPU load
sudo apt install stress -y

# Generate CPU activity for monitoring validation
stress --cpu 1 --timeout 15

# Check running processes
top

# View system uptime
uptime

# View system information
uname -a

# Inspect Azure Linux Agent service logs
journalctl -u walinuxagent

# Exit SSH session
exit
```

## Purpose

The stress test generated short-lived CPU activity that could be observed through the monitoring environment.

The remaining commands supported basic VM and Azure Linux Agent validation during troubleshooting.

These commands are operational lab utilities rather than security controls themselves.
