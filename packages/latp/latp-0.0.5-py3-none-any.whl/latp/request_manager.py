# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu


from .http_request import HttpRequest
from .websocket_request import WebSocketRequest


class RequestManager:
    """
    请求管理器，统一管理和调度不同类型的请求。
    """

    def __init__(self):
        self.http_request = HttpRequest()
        self.websocket_request = WebSocketRequest()

    def send_http(self, method, url, **kwargs):
        """
        发送 HTTP 请求。

        Args:
            method: HTTP 方法。
            url: 请求的 URL。
            kwargs: 其他可选参数。

        Returns:
            requests.Response 对象。
        """
        return self.http_request.send(method, url, **kwargs)

    def send_websocket(self, *args, **kwargs):
        """
        发送 WebSocket 请求。

        Args:
            args: 可选参数。
            kwargs: 可选参数。
        """
        return self.websocket_request.send(*args, **kwargs)
