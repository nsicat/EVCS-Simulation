### EVSE Client (Electric Vehicle Supply Equipment)

import socket
import json
import time
import ssl

class EVSE:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.client = None
        self.connector_id = 1  # Simple connector ID
        self.id_tag = "EV12345"  # Example ID tag
        
        # SSL context setup for development
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = False  # For development only
        self.context.verify_mode = ssl.CERT_NONE  # For development only
        
        # In production, use these settings instead:
        # self.context.load_verify_locations(cafile='certs/ca.crt')
        # self.context.verify_mode = ssl.CERT_REQUIRED
        # self.context.check_hostname = True

    def connect(self):
        try:
            # Create a TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap the socket with SSL/TLS
            self.client = self.context.wrap_socket(sock, server_hostname=self.host)
            
            # Connect to the server
            self.client.connect((self.host, self.port))
            print("✅ Secure connection established with CSMS")
            print(f"Using cipher: {self.client.cipher()}")
            
            self.start_transaction()
            self.stop_transaction()
            
        except ssl.SSLError as e:
            print(f"❌ SSL/TLS handshake failed: {e}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        finally:
            if self.client:
                self.client.close()

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