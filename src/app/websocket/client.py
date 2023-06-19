from __future__ import annotations
import rel
import websocket as ws


class WebsocketClient:
    URI: str = "ws://127.0.0.1:8000"

    def __init__(self):
        self.__websocket: ws.WebSocketApp | None = None

    def __on_open(self, websocket) -> None:
        pass

    def __on_close(self, websocket, close_status_code, close_message) -> None:
        pass

    def __on_message(self, websocket, message) -> None:
        pass

    def __on_error(self, websocket, error) -> None:
        pass

    def run(self):
        ws.enableTrace(True)
        self.__websocket = ws.WebSocketApp(WebsocketClient.URI,
                                           on_open=self.__on_open,
                                           on_close=self.__on_close,
                                           on_message=self.__on_message,
                                           on_error=self.__on_error)
        self.__websocket.run_forever(dispatcher=rel)