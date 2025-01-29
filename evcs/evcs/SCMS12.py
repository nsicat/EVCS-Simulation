import socket
import json

# SCMS Client (manages transactions)
def scms_client():
    host = "127.0.0.1"
    port = 12345
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Connected to EVSE.")
    
    # Start a transaction
    start_transaction = {
        "type": "StartTransaction",
        "connectorId": 1,
        "idTag": "EV12345"
    }
    client.send(json.dumps(start_transaction).encode('utf-8'))
    
    response = client.recv(1024).decode('utf-8')
    print(f"Response from EVSE: {json.loads(response)}")
    
    # Stop a transaction
    stop_transaction = {
        "type": "StopTransaction",
        "transactionId": 1
    }
    client.send(json.dumps(stop_transaction).encode('utf-8'))
    
    response = client.recv(1024).decode('utf-8')
    print(f"Response from EVSE: {json.loads(response)}")
    
    client.close()
    print("Disconnected from EVSE.")

if __name__ == "__main__":
    scms_client()