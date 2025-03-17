# EVCS MITM Attack Simulation

A project to simulate and mitigate Man-in-the-Middle (MITM) attacks in Electric Vehicle Charging Station (EVCS) environments.

## Team Members
- Raul Lopez
- Nico Sicat
- Enoch Elumba

## Project Overview
This project simulates the communication between an Electric Vehicle Charging Station (EVCS) and a Charging Station Management System (CSMS), along with tools to demonstrate MITM attacks and security implementations.

## Directory Structure
```
EVCS-Simulation/
├── CSMS.py              # Charging Station Management System
├── CSMS_enc.py          # Encrypted version of CSMS (Diffie-Hellman + AES)
├── EVCS.py              # Electric Vehicle Charging Station
├── EVSE_enc.py          # Encrypted version of EVCS (Diffie-Hellman + AES)
├── TCSMS.py             # Test CSMS implementation (TLS)
├── TEVCS.py             # Test EVCS implementation (TLS)
├── requirements.txt     # Python dependencies
├── setup.sh            # Setup script
├── MITM_attack.md      # MITM attack documentation
├── encryption.md       # Encryption documentation
```

## Prerequisites

1. Python 3.10
2. Three Virtual Machines:
   - VM1: Debian (CSMS)
   - VM2: Debian (EVSE)
   - VM3: Kali Linux (Attacker)
3. Ettercap (pre-installed on Kali Linux)

### Installing Ettercap
Ettercap should be pre-installed on Kali Linux. If not, install it using:
```bash
sudo apt update
sudo apt install ettercap-graphical -y
```

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd EVCS-Simulation
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

## Virtual Machine Configuration

### VM Setup Requirements
1. **CSMS VM (Debian)**:
   - Install Debian OS
   - Run `CSMS.py` or encrypted versions
   - Configure network settings

2. **EVSE VM (Debian)**:
   - Install Debian OS
   - Run `EVCS.py` or encrypted versions
   - Configure network settings

3. **Attacker VM (Kali Linux)**:
   - Install Kali Linux
   - Ensure Ettercap is installed
   - Configure for network monitoring

### Network Configuration
1. **CSMS VM**:
   - Modify `self.host` in `CSMS.py` to "0.0.0.0" to accept connections from any IP

2. **EVSE VM**:
   - Modify `self.host` in `EVCS.py` to point to CSMS VM's IP address

## Encryption Methods

### Method 1: TLS-Based Encryption (`TCSMS.py` and `TEVCS.py`)
This implementation uses Transport Layer Security (TLS) with SSH tunneling for MITM protection.

**Key Features:**
- Certificate-based authentication
- TLS encryption
- SSH tunneling for ARP spoofing mitigation
- Error handling mechanisms

**Benefits:**
- Secure communication with certificate verification
- Protection against MITM attacks through SSH tunneling
- Data integrity and authenticity verification
- ARP spoofing mitigation in OSI Layer 2

### Method 2: Diffie-Hellman with AES (`CSMS_enc.py` and `EVSE_enc.py`)
This implementation uses Diffie-Hellman key exchange with AES encryption for secure communication.

**Key Features:**
- Diffie-Hellman key exchange for secure key sharing
- AES encryption for data protection
- Secure key exchange without direct transmission
- Implementation using cryptography.hazmat.primitives

**Benefits:**
- Secure key exchange without transmitting the actual key
- Strong encryption through AES
- Protection against unauthorized access
- Data confidentiality and integrity

## Running the Simulation

1. Start the CSMS (choose one version):
```bash
python3 CSMS.py          # Basic version
python3 CSMS_enc.py      # Diffie-Hellman + AES version
python3 TCSMS.py         # TLS version
```

2. Start the EVCS (choose corresponding version):
```bash
python3 EVCS.py          # Basic version
python3 EVSE_enc.py      # Diffie-Hellman + AES version
python3 TEVCS.py         # TLS version
```

## Documentation

- See `MITM_attack.md` for detailed MITM attack setup and execution
- See `encryption.md` for encryption implementation details

## Security Notice

This project is for educational purposes only. Do not use these attack demonstrations on production systems or without proper authorization.
