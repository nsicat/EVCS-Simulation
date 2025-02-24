import asyncio
import websockets
import logging
from ocpp.routing import on
from ocpp.v16 import call_result
from datetime import datetime, timezone
from ocpp.v16 import ChargePoint as cp

logging.basicConfig(level=logging.DEBUG)

class ChargePoint(cp):
    """Handles OCPP messages for the charge point."""
    def __init__(self, id, websocket):
        super().__init__(id, websocket)
        


    @on("StartTransaction")
    async def on_start_transaction(self, id_tag, connector_id, meter_start, timestamp, **kwargs):
        """Handles an incoming StartTransaction request from CSMS."""
        print(f"⚡ Received StartTransaction from CSMS: id_tag={id_tag}, connector_id={connector_id}")

        # Respond with a successful transaction start
        response = call_result.StartTransaction(
            transaction_id=1234,  # Simulated transaction ID
            id_tag_info={"status": "Accepted"}
        )
        return response
    
    @on("BootNotification")
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        """Handles an incoming BootNotification request."""
        print(f"📡 Received BootNotification: Model={charge_point_model}, Vendor={charge_point_vendor}")

        # Respond with an accepted BootNotification response
        response = call_result.BootNotification(
            current_time=datetime.now(timezone.utc).isoformat(),  # Use timezone-aware UTC time
            interval=3,  # The EVSE should send heartbeat every 10 seconds
            status="Accepted",
        )
        return response

async def on_connect(websocket, path=None):
    """Handles new WebSocket connections."""
    charge_point = ChargePoint("EVSE1", websocket)
    await charge_point.start()

async def main():
    """Starts the EVSE WebSocket server."""
    server = await websockets.serve(on_connect, "localhost", 9000, subprotocols=["ocpp1.6"])
    print("🚀 EVSE Server running on ws://localhost:9000")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
