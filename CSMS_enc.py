import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class CSMS:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 12345
        self.server = None
        self.conn = None
        self.addr = None
        self.shared_key = None

    def generate_dh_parameters(self):
        # Generate Diffie-Hellman parameters
        parameters = dh.generate_parameters(generator=2, key_size=2048)
        return parameters

    def generate_dh_keys(self, parameters):
        # Generate private and public keys
        private_key = parameters.generate_private_key()
        public_key = private_key.public_key()
        return private_key, public_key

    def derive_shared_key(self, private_key, peer_public_key):
        # Derive the shared secret key
        shared_key = private_key.exchange(peer_public_key)
        return shared_key[:32]  # Use the first 32 bytes for AES-256

    def encrypt(self, data):
        # Encrypt data using AES
        cipher = AES.new(self.shared_key, AES.MODE_ECB)
        return cipher.encrypt(pad(data.encode(), AES.block_size))

    def decrypt(self, encrypted_data):
        ## Decrypt data using AES
        cipher = AES.new(self.shared_key, AES.MODE_ECB)
        return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()

    def start(self):
        # Start the CSMS server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print("CSMS is waiting for EVSE connection...")

        self.conn, self.addr = self.server.accept()
        print(f"EVSE connected")

        # Perform Diffie-Hellman key exchange
        parameters = self.generate_dh_parameters()
        private_key, public_key = self.generate_dh_keys(parameters)

        # Send parameters and public key to EVSE
        self.conn.send(parameters.parameter_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.ParameterFormat.PKCS3
        ))
        self.conn.send(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

        # Receive EVSE's public key
        evse_public_key = serialization.load_pem_public_key(
            self.conn.recv(4096)
        )

        # Derive shared key
        self.shared_key = self.derive_shared_key(private_key, evse_public_key)
        print("Shared key derived")

        # Communicate securely
        while True:
            encrypted_data = self.conn.recv(1024)
            if not encrypted_data:
                break

            # Decrypt the message
            decrypted_data = self.decrypt(encrypted_data)
            print(f"Received from EVSE: {decrypted_data}")

            # Encrypt a response
            response = "Message received by CSMS"
            encrypted_response = self.encrypt(response)
            self.conn.send(encrypted_response)

        self.stop()

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

