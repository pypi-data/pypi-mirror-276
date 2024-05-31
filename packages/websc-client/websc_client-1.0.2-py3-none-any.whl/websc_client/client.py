"""
The client mediates communication with the WebSC server.
After the communication is established,
the `devices` dictionary is filled in,
from which you can get objects of the `WebSC` type that can be used to control LedSC.
"""
import asyncio
import logging
import json

import websockets as websocket
from websockets import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedOK, WebSocketException

from .exceptions import WebSClientConnectionError
from .websc import WebSCAsync, WebSClientAsyncTemplate

_LOGGER = logging.getLogger(__name__)


class WebSClientAsync(WebSClientAsyncTemplate):
    def __init__(self, host: str, port: int):
        super().__init__(host=host, port=port)
        self._observer_running = False
        self._client: WebSocketClientProtocol | None = None

    async def connect(self):
        """
        Connect to WebSC.

        Read configuration from initial message and create LedSC devices.
        Create background task for websocket listening.
        """
        if self._client is not None and not self._client.closed:
            raise WebSClientConnectionError(f"LedSClient: Already connected to {self.host}:{self.port}")
        _LOGGER.debug(f"LedSClient: Connecting to %s:%s", self.host, self.port)

        try:
            self._client = await websocket.connect(f"ws://{self.host}:{self.port}", open_timeout=2)
        except (OSError, WebSocketException) as E:
            raise WebSClientConnectionError(
                f"LedSClient: Could not connect to websocket at {self.host}:{self.port}"
            ) from E
        _LOGGER.info(f"LedSClient: Connected to %s:%s", self.host, self.port)
        initial_message = json.loads(await self._client.recv())

        if "dev" in initial_message:
            for name, data in initial_message["dev"].items():
                if name in self.devices:
                    device = self.devices[name]
                    await device.data(value=data)
                    device.client = self._client
                else:
                    self.devices[name] = WebSCAsync(
                        client=self,
                        name=name,
                        data=data,
                    )

        _LOGGER.info(f"LedSClient: devices: %s", list(self.devices.keys()))

    async def observer(self):
        """
        Listen on the WebSC and resending data to the LedSC devices

        It is necessary to start this routine immediately after establishing communication with the server.
        If this is not done, the connection will eventually drop due to non-response to ping.
        Run this background task in the corresponding loop in your application.
        """
        try:
            if self._observer_running:
                _LOGGER.error("WebSClient: Observer already running!")
                return
            self._observer_running = True
            _LOGGER.info("WebSClient: Observer started")
            while True:
                try:
                    _data = json.loads(await self._client.recv())
                    if "dev" in _data:
                        for name, data in _data["dev"].items():
                            if name in self.devices:
                                await self.devices[name].data(data)
                except ConnectionClosedOK:
                    _LOGGER.warning("LedSClient: Connection closed. Reconnecting...")
                    for device in self.devices.values():
                        await device.data({"is_lost": 1})
                    while self._client.closed:
                        try:
                            await self.connect()
                            await asyncio.sleep(1)
                        except WebSClientConnectionError:
                            await asyncio.sleep(5)
        finally:
            self._observer_running = False
            await self.disconnect()

    async def disconnect(self) -> None:
        """ Disconnect from WebSC """
        if self._client:
            await self._client.close()
            _LOGGER.info(f"Disconnected from {self.host}:{self.port}")

    async def send(self, data: dict):
        """ Send data to WebSC in JSON format """
        await self._client.send(json.dumps(data))
