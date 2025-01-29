import socket
import json

# EVSE Server (acts as the charger)
def evse_server():
    host = "127.0.0.1"
    port = 12345
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print("EVSE is waiting for SCMS connection...")
    
    conn, addr = server.accept()
    print(f"SCMS connected from {addr}")
    
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        
        message = json.loads(data)
        print(f"Received from SCMS: {message}")
        
        if message["type"] == "StartTransaction":
            response = {
                "type": "TransactionStarted",
                "status": "Accepted",
                "transactionId": 1
            }
        elif message["type"] == "StopTransaction":
            response = {
                "type": "TransactionStopped",
                "status": "Accepted"
            }
        else:
            response = {
                "type": "Error",
                "message": "Invalid request"
            }
        
        conn.send(json.dumps(response).encode('utf-8'))
    
    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    evse_server()
