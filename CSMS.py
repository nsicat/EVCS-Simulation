### CSMS Server (Central System Management)
import socket
import json
import time

class CSMS:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.server = None
        self.conn = None
        self.addr = None
        self.transaction_id = 1  # Simple transaction ID management

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reuse of the address
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print("CSMS is waiting for 🔋EVSE🔋 connection...")
        
        while True:
            try:
                self.conn, self.addr = self.server.accept()
                print(f"EVSE connected from {self.addr}")
                self.communicate()
            except KeyboardInterrupt:
                print("\nReceived interrupt signal, but continuing to run...")
                continue
            except Exception as e:
                print(f"Connection error: {e}")
                continue
            finally:
                if self.conn:
                    self.conn.close()
                    self.conn = None

    def communicate(self):
        while True:
            try:
                data = self.conn.recv(1024)
                if not data:
                    print("Client disconnected, waiting for new connection...")
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
            except Exception as e:
                print(f"Communication error: {e}")
                break

    def handle_start_transaction(self, message):
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
        self.conn.send(json.dumps(response).encode('utf-8'))
        print(f"Sent response: {json.dumps(response, indent=2)}")

    def send_error_response(self, message):
        error_response = {
            "type": "Error",
            "message": message
        }
        self.send_response(error_response)

    def stop(self):
        if self.conn:
            self.conn.close()
        if self.server:
            self.server.close()
        print("CSMS stopped")

def main():
    csms = CSMS()
    while True:
        try:
            csms.start()
        except KeyboardInterrupt:
            print("\nReceived shutdown signal. Press Ctrl+C again to exit completely...")
            try:
                time.sleep(2)  # Give user time to press Ctrl+C again if they really want to exit
            except KeyboardInterrupt:
                print("\nShutting down CSMS...")
                break
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Restarting server...")
            time.sleep(1)  # Add a small delay before restart
            continue
    
    csms.stop()

if __name__ == "__main__":
    main()