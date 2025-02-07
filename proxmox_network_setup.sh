#!/bin/bash

# This script should be run on each VM after Ubuntu installation

# Determine the VM type
VM_TYPE=$1

# Install necessary packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip net-tools tcpdump

# Network configuration
case $VM_TYPE in
  "csms")
    # CSMS Server setup
    cat << EOF | sudo tee /etc/netplan/00-installer-config.yaml
network:
  version: 2
  ethernets:
    ens18:
      dhcp4: no
      addresses: [10.10.10.10/24]
      gateway4: 10.10.10.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
EOF
    ;;
    
  "evcs")
    # EVCS Client setup
    cat << EOF | sudo tee /etc/netplan/00-installer-config.yaml
network:
  version: 2
  ethernets:
    ens18:
      dhcp4: no
      addresses: [10.10.10.11/24]
      gateway4: 10.10.10.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
EOF
    ;;
    
  "attacker")
    # Attacker machine setup
    sudo apt install -y ettercap-graphical wireshark
    cat << EOF | sudo tee /etc/netplan/00-installer-config.yaml
network:
  version: 2
  ethernets:
    ens18:
      dhcp4: no
      addresses: [10.10.10.12/24]
      gateway4: 10.10.10.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
EOF
    # Enable IP forwarding
    echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
    # Make IP forwarding persistent
    echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
    ;;
    
  *)
    echo "Usage: $0 [csms|evcs|attacker]"
    exit 1
    ;;
esac

# Apply network configuration
sudo netplan apply

echo "Network setup complete for $VM_TYPE"
echo "IP Configuration:"
ip addr show ens18
