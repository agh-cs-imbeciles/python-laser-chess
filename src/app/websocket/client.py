from __future__ import annotations

import json
from threading import Thread
import rel
import websocket as ws
from common import MessageType


class WebSocketClientMeta(type):
    _instances: dict[WebSocketClientMeta, WebSocketClient] = {}

    def __call__(cls, *args, **kwargs) -> WebSocketClient:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WebSocketClient(metaclass=WebSocketClientMeta):
    URI: str = "ws://127.0.0.1:8000"

    def __init__(self):
        self.__websocket: ws.WebSocketApp | None = None

    def __on_open(self, websocket) -> None:
        print("Opening the websocket connection")

    def __on_close(self, websocket, close_status_code, close_message) -> None:
        print("Closing the websocket connection")
        print(f"Close status code: {close_status_code}")
        print(f"Close message: {close_message}")

    def __on_message(self, websocket, message) -> None:
        print(f"Received message from the server: {message}")

    def __on_error(self, websocket, error) -> None:
        pass

    def run(self) -> None:
        """
        Open a new web socket and run it until closing the application.
        :return: None
        """

        def __run():
            ws.enableTrace(True)
            self.__websocket = ws.WebSocketApp(WebSocketClient.URI,
                                               on_open=self.__on_open,
                                               on_close=self.__on_close,
                                               on_message=self.__on_message,
                                               on_error=self.__on_error)
            self.__websocket.run_forever(reconnect=5)

        # rel.signal(2, rel.abort)
        # rel.dispatch()

        thread = Thread(target=__run)
        thread.start()

    def create_game(self):
        message = {
            "messageType": str(MessageType.CREATE)
        }
        self.__websocket.send(json.dumps(message))
