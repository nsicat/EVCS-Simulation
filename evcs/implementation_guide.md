# EVCS Simulation Explanation

## Overview of the Simulation
This document explains the interaction between the EVSE (Electric Vehicle Supply Equipment) and CSMS (Charging Station Management System) in our simulation using the OCPP 1.6 protocol.

## Key Components

### 1. EVSEra.py (Server)
- Acts as the charging station (EVSE) server
- Implements OCPP 1.6 protocol over WebSocket
- Listens on `ws://localhost:9000`
- Handles incoming OCPP messages:
  - BootNotification: Initial handshake when EVSE starts up
  - StartTransaction: Handles start charging requests
- Uses the `ocpp.v16` library for protocol implementation
- Responds with standardized OCPP responses using `call_result`

### 2. simulateR.py (Client)
- Acts as the CSMS (Charging Station Management System) client
- Connects to the EVSE server using WebSocket
- Sends OCPP requests:
  1. BootNotification: Identifies itself to the EVSE
  2. StartTransaction: Requests to start a charging session
- Handles responses from the EVSE server

## Communication Flow

1. Server Startup:
```
EVSEra.py starts WebSocket server on port 9000
↓
Waits for incoming connections
```

2. Client Connection:
```
simulateR.py connects to ws://localhost:9000
↓
Connection established with OCPP 1.6 subprotocol
```

3. Transaction Flow:
```
Client → Server: StartTransaction request
(includes connector_id, id_tag, meter_start, timestamp)
↓
Server processes request
↓
Server → Client: StartTransaction response
(includes transaction_id and status)
```

## OCPP Protocol Usage
- Uses OCPP 1.6 standard
- Implements core OCPP messages:
  - BootNotification
  - StartTransaction
- WebSocket communication with subprotocol "ocpp1.6"
- Proper message formatting following OCPP specification

## Implementation Details

### Server-side (EVSEra.py):
```python
@on("StartTransaction")
async def on_start_transaction(self, id_tag, connector_id, meter_start, timestamp):
    return call_result.StartTransaction(
        transaction_id=1234,
        id_tag_info={"status": "Accepted"}
    )
```

### Client-side (simulateR.py):
```python
start_transaction = call.StartTransaction(
    connector_id=1,
    id_tag="EV123",
    meter_start=0,
    timestamp=datetime.utcnow().isoformat()
)
```

## Current Status
- Basic OCPP communication is working
- Successfully simulates:
  - EVSE server startup
  - CSMS client connection
  - Transaction initiation
  - Response handling
- Provides foundation for implementing security measures and attack scenarios

## Next Steps
1. Implement more OCPP messages (StopTransaction, MeterValues)
2. Add security measures (TLS, authentication)
3. Simulate various attack scenarios
4. Implement mitigation strategies
