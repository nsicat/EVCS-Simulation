### EVSE Client (Electric Vehicle Supply Equipment)

import socket
import json
import time

class EVSE:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.client = None
        self.connector_id = 1  # Simple connector ID
        self.id_tag = "EV12345"  # Example ID tag

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print("EVSE connected to SCMS")
        
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
        print(f"Response from SCMS: {json.dumps(json.loads(response), indent=2)}")
        
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
        print(f"Response from SCMS: {json.dumps(json.loads(response), indent=2)}")

    def close(self):
        if self.client:
            self.client.close()
            print("EVSE disconnected from SCMS")

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