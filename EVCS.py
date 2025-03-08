"""
EVSE (Electric Vehicle Supply Equipment) Client Implementation
This module implements a simplified version of an OCPP (Open Charge Point Protocol) client
that simulates an EV charging station communicating with a central management system.

The client simulates basic charging operations:
- Connecting to central system
- Starting charging sessions
- Simulating charging time
- Stopping charging sessions
"""

import socket
import json
import time

class EVSE:
    """
    Electric Vehicle Supply Equipment client class that simulates a charging station.
    Implements a TCP client to communicate with the CSMS (Central System Management Server).
    """
    def __init__(self):
        """
        Initialize EVSE client with default connection settings and identification parameters.
        Sets up connection details and basic charging station parameters.
        """
        self.host = "127.0.0.1"
        self.port = 12345
        self.client = None
        self.connector_id = 1  # Simple connector ID
        self.id_tag = "EV12345"  # Example ID tag

    def connect(self):
        """
        Establish connection with the CSMS server and initiate a charging sequence.
        Performs a complete charging cycle (start -> simulate charging -> stop).
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print("EVSE connected to CSMS")
        
        self.start_transaction()
        self.stop_transaction()

    def start_transaction(self):
        """
        Initiate a charging transaction with the CSMS.
        
        Sends a StartTransaction request with:
        - connectorId: Identifier for the charging connector
        - idTag: Authentication tag for the charging session
        
        Simulates a charging session with a 10-second duration.
        """
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
        """
        End a charging transaction with the CSMS.
        
        Sends a StopTransaction request with:
        - transactionId: Identifier for the charging session to stop
        
        Performs a complete charging cycle (start -> simulate charging -> stop).
        """
        stop_transaction = {
            "type": "StopTransaction",
            "transactionId": 1  # Assuming the transaction ID from start response
        }
        
        print(f"Sending stop transaction: {json.dumps(stop_transaction, indent=2)}")
        self.client.send(json.dumps(stop_transaction).encode('utf-8'))
        
        response = self.client.recv(1024).decode('utf-8')
        print(f"Response from CSMS: {json.dumps(json.loads(response), indent=2)}")

    def close(self):
        """
        Clean up client resources and close the connection to CSMS.
        """
        
        if self.client:
            self.client.close()
            print("EVSE disconnected from CSMS")

def main():
    """
    Main entry point for the EVSE client.
    Handles client startup, charging simulation, and graceful shutdown.
    """
    evse = EVSE()
    try:
        evse.connect()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        evse.close()

if __name__ == "__main__":
    main()