from __future__ import annotations
import json
import secrets
import asyncio
import websockets
from common import MessageStatus, MessageType
from utils import BoardVector2d
from game import Game
from game.piece import Piece


class Server:
    def __init__(self):
        self.__games: list[Game] = []
        self.__connected: list[any] = []
        self.__move: int = 0

    async def start(self, websocket):
        """
        Handle a connection from the first player. Start a new game.
        """

        print("Starting a new game...")

        game: Game = Game()
        self.__games.append(game)

        # join_key: str = secrets.token_urlsafe(8)
        self.__connected.append(websocket)

        try:
            response = {
                "status": str(MessageStatus.SUCCESS),
                "messageType": str(MessageType.INIT),
                # "joinKey": join_key
            }
            await websocket.send(json.dumps(response))
        finally:
            self.__connected.remove(websocket)

    async def join(self, websocket):
        """
        Handle a connection from the second player. Join an existing game.
        """

        # try:
        #     game, connected = JOIN[join_key]
        # except KeyError:
        #     await error(websocket, "Game not found.")
        #     return
        # Register to receive moves from this game.

        print("Joining an existing game...")

        game: Game = self.__games[0]
        self.__connected.append(websocket)

        try:
            # # Send the first move, in case the first player already played it.
            # await replay(websocket, game)
            response = {
                "status": str(MessageStatus.SUCCESS),
                "messageType": str(MessageType.INIT),
                # "joinKey": join_key
            }
            await websocket.send(json.dumps(response))

            # await self.play(websocket, game)
        finally:
            self.__connected.remove(websocket)

    async def play(self, move: dict[any, any], game: Game):
        """
        Receive and process moves from a player.
        """

        print("Receive a move from player")

        origin: BoardVector2d = BoardVector2d.from_str(move["origin"])
        destination: BoardVector2d = BoardVector2d.from_str(move["destination"])
        piece: Piece = game.board.get_piece(origin)
        game.move_piece(piece, destination)

        self.__move += 1

        # try:
        #     # Play the move.
        #     row = game.play(player, column)
        # except RuntimeError as exc:
        #     # Send an "error" event if the move was illegal.
        #     await error(websocket, str(exc))
        #     continue

        response = {
            "status": str(MessageStatus.SUCCESS),
            "messageType": str(MessageType.MOVE),
            "data": game.get_last_move().to_dict()
        }

        websockets.broadcast(self.__connected, json.dumps(response))

        # If move is winning, send a "win" event.
        # if game.winner is not None:
        #     event = {
        #         "type": "win",
        #         "player": game.winner,
        #     }
        #
        # websockets.broadcast(connected, json.dumps(event))

    async def handler(self, websocket):
        """
        Handle a connection and dispatch it according to who is connecting.
        """

        message_plain = await websocket.recv()
        message = json.loads(message_plain)
        assert message["messageType"], "Message type hasn't been sent"

        match MessageType.from_str(message["messageType"]):
            case MessageType.INIT:
                if not self.__connected:
                    await self.start(websocket)
                elif len(self.__connected) == 1:
                    await self.join(websocket)
            case MessageType.MOVE:
                # await self.play(message["data"], self.__games[0])
                pass

        # if "join" in event:
        #     # Second player joins an existing game
        #     await join(websocket, event["join"])
        # elif "watch" in event:
        #     # Spectator watches an existing game
        #     await watch(websocket, event["watch"])
        # else:
        #     # First player starts a new game
        #     await start(websocket)

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
