import asyncio
import websockets


async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(f"<<< {message}")
            response = "Bishops suck"
            print(f">>> {response}")
            await websocket.send(response)
        except websockets.ConnectionClosedOK:
            break


async def main():
    async with websockets.serve(handler, "", 8000):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
