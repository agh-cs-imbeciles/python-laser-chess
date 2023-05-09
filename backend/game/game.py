import asyncio
import websockets


async def handler(websocket):
    message = await websocket.recv()
    print(f"<<< {message}")
    response = "Bishops sucks"
    print(f">>> {response}")
    await websocket.send(response)
    # while True:
    #     try:
    #         message = await websocket.recv()
    #     except websockets.ConnectionClosedOK:
    #         break
    #     print(message)


async def main():
    async with websockets.serve(handler, "", 8000):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
