from scapy.all import send

def forward_packet(packet, target_ip, target_port):
    """
    Forward the captured packet to its intended recipient after modification.
    """
    packet[IP].dst = target_ip
    packet[TCP].dport = target_port
    send(packet)
