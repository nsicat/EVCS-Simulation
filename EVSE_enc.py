import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class EVSE:
    def __init__(self):
        self.host = "127.0.0.1"  # CSMS IP address
        self.port = 12345
        self.client = None
        self.shared_key = None

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
        # Decrypt data using AES
        cipher = AES.new(self.shared_key, AES.MODE_ECB)
        return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        # Perform Diffie-Hellman key exchange
        # Receive parameters from CSMS
        parameters = serialization.load_pem_parameters(
            self.client.recv(4096)
        )
        private_key, public_key = self.generate_dh_keys(parameters)

        # Receive CSMS's public key
        csms_public_key = serialization.load_pem_public_key(
            self.client.recv(4096)
        )

        # Send EVSE's public key to CSMS
        self.client.send(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

        # Derive shared key
        self.shared_key = self.derive_shared_key(private_key, csms_public_key)
        print("Shared key derived")

        # Send an encrypted message
        message = "Hello, CSMS!"
        encrypted_message = self.encrypt(message)
        self.client.send(encrypted_message)

        # Receive an encrypted response
        encrypted_response = self.client.recv(1024)
        decrypted_response = self.decrypt(encrypted_response)
        print(f"Response from CSMS: {decrypted_response}")

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
