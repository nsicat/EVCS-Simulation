from scapy.all import sniff

def packet_callback(packet):
    print(packet.show())  # Display captured packet details

# Sniff TCP packets on localhost
print("Listening for EVSE-CSMS traffic...")
sniff(filter="tcp", iface="lo", prn=packet_callback, store=0)