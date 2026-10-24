import asyncio
import json
import os
import websockets

async def handle_sip_call(call_id: str):
    async with websockets.connect(
        f"wss://api.x.ai/v1/realtime?call_id={call_id}",
        additional_headers={"Authorization": f"Bearer {os.environ['XAI_API_KEY']}"},
    ) as ws:
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "voice": "eve",
                "instructions": "You are a helpful phone support agent.",
                "turn_detection": {"type": "server_vad"},
            },
        }))
        await ws.send(json.dumps({"type": "response.create"}))

        async for msg in ws:
            event = json.loads(msg)
            print(event["type"])

asyncio.run(handle_sip_call("00000000-0000-0000-0000-000000000000"))
