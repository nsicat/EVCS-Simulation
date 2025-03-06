### EVSE Client (Electric Vehicle Supply Equipment)

import socket
import json
import time
import ssl

class EVSE:
    def __init__(self):
        self.host = "192.168.64.2"
        self.port = 12345
        self.client = None
        self.connector_id = 1  # Simple connector ID
        self.id_tag = "EV12345"  # Example ID tag

       # TLS configuration
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_cert_chain(certfile="evcs_cert.pem", keyfile="evcs_key.pem")
        self.context.load_verify_locations(cafile="csms_cert.pem")  # Verify CSMS certificate
        self.context.verify_mode = ssl.CERT_REQUIRED  # Require server certificate

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Wrap the socket with TLS
        self.client = self.context.wrap_socket(self.client, server_hostname="CSMS")
        self.client.connect((self.host, self.port))
        print("EVSE connected to CSMS")
        
        self.start_transaction()
        self.stop_transaction()

    def start_transaction(self):
        # Create start transaction message
        start_transaction = {
            "type": "StartTransaction",
            "connectorId": self.connector_id,
            "idTag": self.id_tag
        }
        
        print(f"Sending start transaction: {json.dumps(start_transaction, indent=2)}")
        self.client.send(json.dumps(start_transaction).encode('utf-8'))
        
        response = self.client.recv(1024).decode('utf-8')
        print(f"Response from CSMS: {json.dumps(json.loads(response), indent=2)}")
        
        # Simulate charging time
        print("Charging in progress...")
        time.sleep(10)  # Simulate charging time

    def stop_transaction(self):
        # Create stop transaction message
        stop_transaction = {
            "type": "StopTransaction",
            "transactionId": 1  # Assuming the transaction ID from start response
        }
        
        print(f"Sending stop transaction: {json.dumps(stop_transaction, indent=2)}")
        self.client.send(json.dumps(stop_transaction).encode('utf-8'))
        
        response = self.client.recv(1024).decode('utf-8')
        print(f"Response from CSMS: {json.dumps(json.loads(response), indent=2)}")

    def close(self):
        if self.client:
            self.client.close()
            print("EVSE disconnected from CSMS")

def main():
    evse = EVSE()
    try:
        evse.connect()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        evse.close()

if __name__ == "__main__":
    main()

#openssl req -x509 -newkey rsa:4096 -keyout evcs_key.pem -out evcs_cert.pem -days 365 -nodes -subj "/CN=EVCS"
#scp evcs_cert.pem user@CSMS_VM:/path/to/evcs_cert.pem
