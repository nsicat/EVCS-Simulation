# EVCS MITM Attack Simulation

A project to simulate and mitigate Man-in-the-Middle (MITM) attacks in Electric Vehicle Charging Station (EVCS) environments.

## Team Members
- Raul Lopez
- Nico Sicat
- Enoch Elumba

## Project Overview
This project simulates potential MITM attacks on the communication between Electric Vehicle Supply Equipment (EVSE) and Smart Charging Management Systems (SCMS). It includes both attack demonstrations and mitigation strategies.

## Components
- `evcs/`: Core EVCS simulation components
  - `evse.py`: Electric Vehicle Supply Equipment simulation
  - `scms.py`: Smart Charging Management System simulation
  - `attacker.py`: MITM attack simulation
- `security/`: Security and mitigation implementations
  - `encryption.py`: Encryption utilities
  - `authentication.py`: Authentication mechanisms
- `simulation/`: Simulation scenarios and runners
- `tests/`: Test cases and validation

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
[Documentation to be added]

## Security Considerations
This project is for educational purposes only. The simulated attacks should only be performed in controlled, isolated environments.
