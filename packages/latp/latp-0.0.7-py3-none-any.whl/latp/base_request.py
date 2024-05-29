# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu

class BaseRequest:
    """
    基类，用于定义请求接口和通用功能。
    所有具体的请求类应继承此类，并实现 `send` 方法。
    """
    def send(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method")