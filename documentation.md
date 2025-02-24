# TLS Implementation for EVCS-CSMS Communication

## Overview
This document outlines the implementation of TLS (Transport Layer Security) encryption for the communication between the Electric Vehicle Charging Station (EVCS) and the Charging Station Management System (CSMS). This security enhancement ensures that all JSON messages exchanged between these components are encrypted during transmission.

## Implementation Details

### 1. Certificate Generation
For development/testing purposes, we use self-signed certificates. In production, these should be replaced with certificates from a trusted Certificate Authority (CA).

Required files:
- `server.key`: Private key for the CSMS server
- `server.crt`: Public certificate for the CSMS server
- `ca.crt`: Certificate Authority certificate

### 2. Code Changes

#### CSMS Server Changes
- Implemented SSL context creation with server certificate and private key
- Added TLS socket wrapping for secure communication
- Added error handling for SSL/TLS handshake failures
- Added cipher information logging
- Current cipher: TLS_AES_256_GCM_SHA384 with TLSv1.3

Key code changes:
```python
# SSL context setup
self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
self.context.load_cert_chain(
    certfile='certs/server.crt',
    keyfile='certs/server.key'
)
```

#### EVCS Client Changes
- Implemented SSL context for server authentication
- Added TLS socket wrapping for secure communication
- Added error handling for connection failures
- Added cipher information logging

Key code changes:
```python
# SSL context setup
self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
self.context.load_verify_locations(cafile='certs/ca.crt')  # For production
```

### 3. Security Features
- **Protocol**: Using TLS 1.3 (most secure version)
- **Cipher Suite**: TLS_AES_256_GCM_SHA384
  - AES-256: Symmetric encryption for data
  - GCM (Galois/Counter Mode): Provides both authentication and encryption
  - SHA384: Secure hashing algorithm for message integrity
- **Perfect Forward Secrecy**: Provided by TLS 1.3
- **Message Encryption**: All JSON messages are encrypted in transit
- **Protection**: Secure against MITM (Man-in-the-Middle) attacks

### 4. Development vs Production Settings

#### Development Mode
```python
# Less strict settings for testing
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
```

#### Production Mode
```python
# Strict security settings
context.check_hostname = True
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile='certs/ca.crt')
```

### 5. Testing Results
- Successful TLS handshake between CSMS and EVCS
- Encrypted communication verified
- JSON messages securely transmitted
- All charging transactions completed successfully over encrypted channel

### 6. Security Considerations
1. **Certificate Management**:
   - Keep private keys secure
   - Never commit certificates to version control
   - Use proper certificate rotation procedures
   - Monitor certificate expiration dates

2. **Production Deployment**:
   - Use certificates from trusted CAs
   - Enable strict certificate verification
   - Enable hostname verification
   - Consider implementing mutual TLS (mTLS)

3. **Monitoring**:
   - Log TLS handshake failures
   - Monitor for certificate expiration
   - Track cipher suite usage
   - Alert on security-related events

4. **Maintenance**:
   - Regular certificate rotation
   - Regular security audits
   - Keep TLS libraries updated
   - Monitor for security vulnerabilities

## Future Enhancements
1. Implement mutual TLS authentication (mTLS)
2. Add certificate pinning
3. Implement automatic certificate rotation
4. Add security event logging and monitoring
5. Implement certificate revocation checking

## Setup Instructions

1. Generate certificates (for development):
```bash
# Generate CA key and certificate
openssl req -x509 -newkey rsa:4096 -days 365 -nodes -keyout ca.key -out ca.crt -subj "/CN=EVCS-CA"

# Generate server key and CSR
openssl req -newkey rsa:4096 -nodes -keyout server.key -out server.csr -subj "/CN=CSMS-Server"

# Sign server certificate with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365
```

2. Place certificates in a `certs` directory:
```
certs/
  ├── ca.crt
  ├── server.key
  └── server.crt
```

3. Update configuration in code to use the certificates

## Testing
- Verify TLS handshake success
- Confirm encrypted communication using Wireshark
- Test certificate validation
- Verify handling of invalid certificates

## Error Handling
The implementation includes proper error handling for:
- Certificate validation failures
- TLS handshake failures
- Connection errors
- Invalid certificates
