import asyncio
import websockets
from ocpp.routing import on
from ocpp.v16 import call_result
from ocpp.v16 import ChargePoint as cp

class ChargePoint(cp):
    """Handles OCPP messages for the charge point."""

    async def start_charging(self, transaction_id: str):
        """Simulates starting a charging session."""
        request = call_result.StartTransaction(
            transaction_id=transaction_id,
            id_tag_info={"status": "Accepted"}
        )
        return request

    @on("StartTransaction")
    async def on_start_transaction(self, **kwargs):
        """Handles an incoming StartTransaction request."""
        print(f"Received charging request: {kwargs}")
        return await self.start_charging(kwargs["transactionId"])

async def on_connect(websocket, path=None):
    """Handles new WebSocket connections."""
    print(f"New connection from {websocket.remote_address} at path {path}")

    charge_point = ChargePoint("EVSE1", websocket)
    await charge_point.start()

async def main():
    """Starts the SCMS WebSocket server."""
    server = await websockets.serve(on_connect, "localhost", 9000)
    print("🚀 SCMS Server running on ws://localhost:9000")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
