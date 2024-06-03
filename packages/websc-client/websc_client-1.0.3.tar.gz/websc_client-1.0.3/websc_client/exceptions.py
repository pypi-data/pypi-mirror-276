class WebSClientError(Exception):
    pass


class WebSClientConnectionError(WebSClientError):
    pass


class WebSClientCallbackError(WebSClientError):
    pass