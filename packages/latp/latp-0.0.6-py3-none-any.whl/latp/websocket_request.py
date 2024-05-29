# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu


from .base_request import BaseRequest


class WebSocketRequest(BaseRequest):
    """
    WebSocket 请求类，继承自 BaseRequest 类。
    目前预留，未来可实现具体的 WebSocket 请求逻辑。
    """

    def __init__(self, base_url=None):
        self.base_url = base_url

    def send(self, *args, **kwargs):
        """
        发送 WebSocket 请求。
        目前预留，未来可实现具体的 WebSocket 请求逻辑。

        Args:
            args: 可选参数。
            kwargs: 可选参数。
        """
        pass
