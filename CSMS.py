"""
CSMS (Central System Management Server) Implementation
This module implements a simplified version of an OCPP (Open Charge Point Protocol) central system
that manages communication with Electric Vehicle Supply Equipment (EVSE).

The server handles basic charging transactions including:
- Starting charging sessions
- Stopping charging sessions
- Basic error handling and response management
"""

### CSMS Server (Central System Management)
import socket
import json
import time

class CSMS:
    """
    Central System Management Server class that handles EVSE connections and charging transactions.
    Implements a basic TCP server to communicate with EVSE clients.
    """
    def __init__(self):
        """Initialize CSMS with default connection settings and transaction management."""
        self.host = "127.0.0.1"
        self.port = 12345
        self.server = None
        self.conn = None
        self.addr = None
        self.transaction_id = 1  # Simple transaction ID management

    def start(self):
        """
        Start the CSMS server and wait for EVSE connections.
        Sets up a TCP socket and listens for incoming connections.
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print("CSMS is waiting for 🔋EVSE🔋 connection...")
        
        self.conn, self.addr = self.server.accept()
        print(f"EVSE connected from {self.addr}")
        
        self.communicate()

    def communicate(self):
        """
        Main communication loop that handles incoming messages from EVSE.
        Processes JSON messages and routes them to appropriate handlers based on message type.
        Supports: StartTransaction, StopTransaction
        """
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            
            try:
                message = json.loads(data.decode('utf-8'))
                print(f"Received from EVSE: {json.dumps(message, indent=2)}")
                
                if message["type"] == "StartTransaction":
                    self.handle_start_transaction(message)
                elif message["type"] == "StopTransaction":
                    self.handle_stop_transaction(message)
                else:
                    self.send_error_response("Invalid request type")
            
            except json.JSONDecodeError:
                print("Invalid JSON received from EVSE")
                self.send_error_response("Invalid JSON format")
            
            except KeyError as e:
                print(f"Missing key in message: {e}")
                self.send_error_response("Missing required fields")

        self.stop()

    def handle_start_transaction(self, message):
        """
        Handle incoming StartTransaction requests from EVSE.
        
        Args:
            message (dict): JSON message containing:
                - connectorId: ID of the charging connector
                - idTag: Authentication tag for the charging session
                
        Returns:
            Sends a TransactionStarted response with a unique transaction ID
        """
        try:
            # Validate input fields
            connector_id = message.get("connectorId")
            id_tag = message.get("idTag")
            
            if not connector_id or not id_tag:
                self.send_error_response("Missing connectorId or idTag")
                return

            # Simulate transaction start
            print(f"Starting transaction for ID Tag: {id_tag}")
            time.sleep(1)  # Simulate processing time
            
            # Send transaction started response
            response = {
                "type": "TransactionStarted",
                "status": "Accepted",
                "transactionId": self.transaction_id,
                "connectorId": connector_id
            }
            self.send_response(response)
            
            self.transaction_id += 1  # Increment transaction ID
            
        except Exception as e:
            self.send_error_response(str(e))

    def handle_stop_transaction(self, message):
        """
        Handle incoming StopTransaction requests from EVSE.
        
        Args:
            message (dict): JSON message containing:
                - transactionId: ID of the transaction to stop
                
        Returns:
            Sends a TransactionStopped response confirming the stop action
        """
        try:
            transaction_id = message.get("transactionId")
            
            if not transaction_id:
                self.send_error_response("Missing transactionId")
                return

            # Simulate transaction stop
            print(f"Stopping transaction ID: {transaction_id}")
            time.sleep(1)  # Simulate processing time
            
            # Send transaction stopped response
            response = {
                "type": "TransactionStopped",
                "status": "Accepted",
                "transactionId": transaction_id
            }
            self.send_response(response)
            
        except Exception as e:
            self.send_error_response(str(e))

    def send_response(self, response):
        """
        Send a JSON-formatted response back to the EVSE.
        
        Args:
            response (dict): Response data to be sent to EVSE
        """
        self.conn.send(json.dumps(response).encode('utf-8'))
        print(f"Sent response: {json.dumps(response, indent=2)}")

    def send_error_response(self, message):
        """
        Send an error response to the EVSE when issues occur.
        
        Args:
            message (str): Error message describing the issue
        """
        error_response = {
            "type": "Error",
            "message": message
        }
        self.send_response(error_response)

    def stop(self):
        """
        Clean up server resources and close all connections.
        """
        if self.conn:
            self.conn.close()
        if self.server:
            self.server.close()
        print("CSMS stopped")

def main():
    """
    Main entry point for the CSMS server.
    Handles server startup and graceful shutdown on interruption.
    """
    csms = CSMS()
    try:
        csms.start()
    except KeyboardInterrupt:
        print("CSMS shutdown requested...")
        csms.stop()
    except Exception as e:
        print(f"Error occurred: {e}")
        csms.stop()

if __name__ == "__main__":
    main()