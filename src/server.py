import json
import asyncio
import websockets
from game import Game
from utils import BoardVector2d


class Server:
    def __init__(self):
        self._games: list[Game] = [Game()]

    async def handler(self, websocket):
        """
        Handle a connection and dispatch it according to who is connecting.
        """

        message_plain = await websocket.recv()
        message = json.loads(message_plain)
        assert event["type"] == "init"

        if "join" in event:
            # Second player joins an existing game.
            await join(websocket, event["join"])
        elif "watch" in event:
            # Spectator watches an existing game.
            await watch(websocket, event["watch"])
        else:
            # First player starts a new game.
            await start(websocket)

        # while True:
        #     try:
        #         message = await websocket.recv()
        #         message_obj = json.loads(message)
        #         print(f"<<< {message_obj}")
        #
        #         game = self._games[0]
        #         origin = BoardVector2d.from_str(message_obj.get("origin"))
        #         destination = BoardVector2d.from_str(message_obj.get("destination"))
        #         game.move_piece(game.board.get_piece(origin), destination)
        #
        #         response = "Bishops suck"
        #         print(f">>> {response}")
        #         await websocket.send(response)
        #     except websockets.ConnectionClosedOK:
        #         break

    async def main(self):
        async with websockets.serve(self.handler, "", 8000):
            await asyncio.Future()


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.main())
