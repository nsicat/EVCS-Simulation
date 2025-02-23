import asyncio
import logging
import websockets
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)


async def on_connect(websocket, path):
    """ Handle connection from charge point and respond to BootNotification. """
    try:
        requested_protocols = websocket.request_headers['Sec-WebSocket-Protocol']
    except KeyError:
        logging.info("Client hasn't requested any Subprotocol. Closing connection")
        return await websocket.close()

    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        logging.warning('Protocols Mismatched | Closing connection')
        return await websocket.close()

    charge_point_id = path.strip('/')
    
    # Handle BootNotification request
    await handle_boot_notification(websocket)


async def handle_boot_notification(websocket):
    """ Handle the BootNotification message and respond. """
    # This is the simplified BootNotification message
    boot_notification = {
        "messageType": "BootNotification",
        "chargePointModel": "EVSE1",
        "chargePointVendor": "EVCS_Vendor",
        "reason": "PowerUp"
    }

    # Send BootNotification to charge point
    logging.info(f"Received BootNotification: {boot_notification}")

    # Respond back to the charge point with BootNotification response
    response = {
        "currentTime": datetime.utcnow().isoformat(),
        "interval": 10,
        "status": "Accepted"
    }
    
    logging.info(f"Sending BootNotification response: {response}")
    await websocket.send(json.dumps(response))


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=["ocpp1.6"]
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
