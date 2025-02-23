import asyncio
import websockets
from datetime import datetime
from ocpp.v16 import call
import logging 
from ocpp.v16 import ChargePoint as cp

logging.basicConfig(level=logging.DEBUG)

class CSMSClient:
    async def connect(self):
        """Connects to the EVSE and sends a StartTransaction request."""
        uri = "ws://localhost:9000/EVSE1"
        try:
            async with websockets.connect(uri, subprotocols=["ocpp1.6"]) as ws:
                charge_point = cp("CSMS1", ws)

                # ✅ Remove the hanging start() call
                print("✅ Connected to EVSE")

                # 🔹 Send BootNotification first
                boot_notification = call.BootNotification(
                    charge_point_model="EVSE1",
                    charge_point_vendor="EVCS_Vendor"
                )

                print("🚀 Sending BootNotification to EVSE...")
                #boot_response = await charge_point.call(boot_notification)
                #print("✅ BootNotification Response:", boot_response)

                #if boot_response["status"] == "Accepted":
                    #print("✅ BootNotification was accepted.")

                # Don't close connection here, keep it open for future interactions
                #await asyncio.sleep(10)  # or another mechanism to keep connection alive
                
                # 🔹 After BootNotification, send StartTransaction
                start_transaction = call.StartTransaction(
                    connector_id=1,
                    id_tag="EV123",
                    meter_start=0,
                    timestamp=datetime.utcnow().isoformat() + "Z",
                )

                print("🔌 Sending StartTransaction request to EVSE...")
                response = await asyncio.wait_for(charge_point.call(start_transaction), timeout=60)  # increase timeout
                print("⚡ Response from EVSE:", response)

        except Exception as e:
            print("🚨 Connection failed:", e)

if __name__ == "__main__":
    asyncio.run(CSMSClient().connect())
