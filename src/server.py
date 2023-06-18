from __future__ import annotations
import json
import asyncio
import websockets

from utils import Key
from common import MessageStatus, MessageType
from utils import BoardVector2d
from game import Game
from game.piece import Piece


class Server:
    def __init__(self):
        self.__games: dict[str, Game] = {}
        self.__connected: dict[str, list[any]] = {}
        self.__move: int = 0

    async def main(self):
        async with websockets.serve(self.handler, "", 8000):
            await asyncio.Future()

    async def create(self, websocket):
        """
        Handle a connection from the first player. Start a new game.
        """

        print("Starting the new game...")

        game_id: str | None = self.__generate_game_id()
        player_id: str | None = self.__generate_player_id()
        game: Game = Game()
        self.__games[game_id] = game
        self.__connected[game_id].append(websocket)

        try:
            response = {
                "status": str(MessageStatus.SUCCESS),
                "messageType": str(MessageType.INIT),
                "gameId": game_id,
                "playerId": player_id
            }
            await websocket.send(json.dumps(response))
        finally:
            self.__connected[game_id].remove(websocket)

    async def join(self, websocket, game_id: str | None):
        """
        Handle a connection from the second player. Join an existing game.
        """

        if not game_id:
            response = {
                "status": str(MessageStatus.ERROR)
            }
            await websocket.send(json.dumps(response))
            raise ValueError("Game ID hasn't been sent")

        print("Joining the existing game...")

        game: Game = self.__games[0]
        self.__connected.append(websocket)

        try:
            response = {
                "status": str(MessageStatus.SUCCESS),
                "messageType": str(MessageType.JOIN),
                "playerId": self.__generate_player_id(),
                "gameId": game_id
            }
            if game.move_number == 1:
                response["data"] = json.dumps(game.get_last_move())
            await websockets.broadcast(self.__connected, response)
        finally:
            self.__connected.remove(websocket)

    async def play(self, move: dict[any, any], player_id: str, game: Game):
        """
        Receive and process moves from a player.
        """

        if "origin" not in move:
            raise ValueError("Move object is invalid, doesn't contain \"origin\" key")
        if "destination" not in move:
            raise ValueError("Move object is invalid, doesn't contain \"destination\" key")

        print(f"Received a move from player", end='')
        origin: BoardVector2d = BoardVector2d.from_str(move["origin"])
        destination: BoardVector2d = BoardVector2d.from_str(move["destination"])
        piece: Piece = game.board.get_piece(origin)
        print(f" [{destination} -> {origin}]")

        game: Game = self.__games[0]

        if game.board.get_piece_movement(origin):
            game.move_piece(piece, destination)
        else:
            response = {
                "status": str(MessageStatus.ERROR)
            }
            websockets.broadcast(self.__connected, json.dumps(response))
            raise ValueError("Sent move is illegal")

        self.__move += 1

        response = {
            "status": str(MessageStatus.SUCCESS),
            "messageType": str(MessageType.MOVE),
            "playerId": player_id,
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
            case MessageType.CREATE:
                await self.create(websocket)
                # elif len(self.__connected) == 1:
                #     await self.join(websocket, message.get("gameId"))
            case MessageType.MOVE:
                assert message["playerId"], "Player ID hasn't been sent"
                player_id: str = message["playerId"]
                await self.play(message["data"], player_id, self.__games[0])

    def __generate_player_id(self) -> str:
        prefix: str = "laschess_pid"
        id: str = Key.generate_timestamp_id(8)
        return f"{prefix}_{id}"

    def __generate_game_id(self) -> str:
        prefix: str = "laschess_gid"
        id: str = Key.generate_timestamp_id(8)
        return f"{prefix}_{id}"


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.main())
