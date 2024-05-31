import inspect
from typing import Callable, Coroutine

from websc_client.exceptions import WebSClientCallbackError


class WebSClientAsyncTemplate:
    def __init__(self, host: str, port: int):
        self.devices: dict[str, WebSCAsync] = {}
        self.host = host
        self.port = port

    async def connect(self):
        """
        Connect to WebSC.

        Read configuration from initial message and create LedSC devices.
        Create background task for websocket listening.
        """
        pass

    async def disconnect(self) -> None:
        """ Disconnect from WebSC ."""
        pass

    async def send(self, data: dict):
        """ Send data to WebSC. """
        pass


DataChangeCallback = Callable[[dict[str, int]], Coroutine]


class WebSCAsync:
    """
    It is used to control the LedSC.
    It is necessary to connect to the WebSC client.
    A callback can be registered for status change events.
    """
    def __init__(self, client: WebSClientAsyncTemplate, name: str, data: dict = None):
        self.client = client
        self.name = str(name)
        self._data = data if data is not None else {}
        self.callback_data_change = None
        self.is_async: bool = bool(inspect.iscoroutinefunction(self.client.send))

    def set_callback(self, callback: DataChangeCallback):
        """
        Setting the callback for event subscription when the device state changes.

        Callback must be asynchronous.
        The input parameter of the callback is a dictionary of changed variables.
        """
        self.callback_data_change = callback

    async def data(self, value: dict):
        """ For update data. This data must be received from WebSC """
        self._data.update(value)
        if self.callback_data_change:
            try:
                await self.callback_data_change(value)
            except Exception as E:
                raise WebSClientCallbackError(f"Error in registered callback: {E}") from E

    async def send(self, data: dict):
        """ Marks the message with identifying characters and sends. """
        await self.client.send({'dev': {self.name: data}})

    async def set_red(self, value: int):
        await self.send({"R": value})

    async def set_green(self, value: int):
        await self.send({"G": value})

    async def set_blue(self, value: int):
        await self.send({"B": value})

    async def set_white(self, value: int):
        await self.send({"W": value})

    async def set_rgb(self, red: int, green: int, blue: int):
        await self.send({"R": red, "G": green, "B": blue})

    async def set_rgbw(self, red: int, green: int, blue: int, white: int):
        await self.send({"R": red, "G": green, "B": blue, "W": white})

    async def set_live_mode(self, value: bool):
        await self.send({"LM": value})

    async def set_transition_time(self, value: float):
        await self.send({"TT": value})

    async def set_pwm_cycle(self, value: int):
        await self.send({"PWMC": value})

    async def set_px_counter(self, value: int):
        await self.send({"PX_CNT": value})

    async def do_px_trigger(self):
        await self.send({"trigger": True})

    @property
    def rgbw(self) -> tuple[int, int, int, int]:
        return (
            self._data["R"],
            self._data["G"],
            self._data["B"],
            self._data["W"],
        )

    @property
    def rgb(self) -> tuple[int, int, int]:
        return (
            self._data["R"],
            self._data["G"],
            self._data["B"],
        )

    @property
    def red(self) -> int:
        return self._data["R"]

    @property
    def green(self) -> int:
        return self._data["G"]

    @property
    def blue(self) -> int:
        return self._data["B"]

    @property
    def white(self) -> int:
        return self._data["W"]

    @property
    def live_mode(self) -> int:
        return self._data["LM"]

    @property
    def transition_time(self) -> int:
        return self._data["TT"]

    @property
    def pwm_cycle(self) -> int:
        return self._data["PWMC"]

    @property
    def px_counter(self) -> int:
        return self._data["PX_CNT"]

    @property
    def is_lost(self) -> int:
        return bool(self._data["is_lost"])
