### CSMS Server (Central System Management)
import socket
import json
import time
import ssl

class CSMS:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.server = None
        self.conn = None
        self.addr = None
        self.transaction_id = 1  # Simple transaction ID management
        
        # SSL context setup for development
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(
            certfile='certs/server.crt',
            keyfile='certs/server.key'
        )
        # For development only
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        
        # In production, use these settings:
        # self.context.load_verify_locations(cafile='certs/ca.crt')
        # self.context.verify_mode = ssl.CERT_REQUIRED

    def start(self):
        # Create a TCP socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print(" CSMS is waiting for secure EVSE connection...")
        
        # Accept connections
        client_socket, self.addr = self.server.accept()
        print(f"EVSE attempting connection from {self.addr}")
        
        try:
            # Wrap the socket with SSL/TLS
            self.conn = self.context.wrap_socket(client_socket, server_side=True)
            print(f" Secure connection established with EVSE at {self.addr}")
            print(f"Using cipher: {self.conn.cipher()}")
            self.communicate()
        except ssl.SSLError as e:
            print(f" SSL/TLS handshake failed: {e}")
            client_socket.close()
        except Exception as e:
            print(f" Error during connection: {e}")
            client_socket.close()

    def communicate(self):
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