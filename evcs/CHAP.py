import asyncio
import logging
import websockets
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class ChargePoint:
    def __init__(self, charge_point_id, websocket):
        self.charge_point_id = charge_point_id
        self.websocket = websocket

    async def send_boot_notification(self):
        # Create a BootNotification-like message
        boot_notification = {
            "messageType": "BootNotification",
            "chargePointModel": "Wallbox XYZ",
            "chargePointVendor": "anewone",
            "reason": "PowerUp"
        }

        # Send BootNotification message to the server
        logging.info(f"Sending BootNotification: {boot_notification}")
        await self.websocket.send(json.dumps(boot_notification))

        # Wait for the server response
        response = await self.websocket.recv()
        response_data = json.loads(response)

        # Check response status
        if response_data.get("status") == "Accepted":
            logging.info("Connected to central system.")
        else:
            logging.warning("BootNotification rejected.")

    async def start(self):
        logging.info(f"ChargePoint {self.charge_point_id} is starting.")
        # Additional code for charge point functionality can be added here


async def main():
    async with websockets.connect(
            'ws://localhost:9000/CP_1',
            subprotocols=["ocpp1.6"]
    ) as ws:
        cp = ChargePoint('CP_1', ws)

        # Start charge point communication and send BootNotification
        await asyncio.gather(cp.start(), cp.send_boot_notification())


if __name__ == '__main__':
    asyncio.run(main())
