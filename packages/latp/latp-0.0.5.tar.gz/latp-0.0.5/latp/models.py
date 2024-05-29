# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu

from enum import Enum
from typing import Any, Callable, Dict, List, Text, Union
from pydantic import BaseModel, HttpUrl

Name = Text
Url = Text
BaseUrl = Union[HttpUrl, Text]
VariablesMapping = Dict[Text, Any]
FunctionsMapping = Dict[Text, Callable]
Headers = Dict[Text, Text]
Cookies = Dict[Text, Text]
Verify = bool
Hooks = List[Union[Text, Dict[Text, Text]]]
Export = List[Text]
Validators = List[Dict]
Env = Dict[Text, Any]


class MethodEnum(Text, Enum):
    """
    HTTP 方法枚举类，定义常见的 HTTP 请求方法。
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class RequestStat(BaseModel):
    """
    请求统计数据类，包含请求的大小、响应时间等信息。
    """
    content_size: float = 0
    response_time_ms: float = 0
    elapsed_ms: float = 0


class AddressData(BaseModel):
    """
    地址数据类，包含客户端和服务器端的 IP 和端口信息。
    """
    client_ip: Text = "N/A"
    client_port: int = 0
    server_ip: Text = "N/A"
    server_port: int = 0


class RequestData(BaseModel):
    """
    请求数据类，包含 HTTP 请求的详细信息。
    """
    method: MethodEnum = MethodEnum.GET
    url: Url
    headers: Headers = {}
    cookies: Cookies = {}
    body: Union[Text, bytes, List, Dict, None] = {}


class ResponseData(BaseModel):
    """
    响应数据类，包含 HTTP 响应的详细信息。
    """
    status_code: int
    headers: Dict
    cookies: Cookies
    encoding: Union[Text, None] = None
    content_type: Text
    body: Union[Text, bytes, List, Dict, None]


class ReqRespData(BaseModel):
    """
    请求和响应数据类，包含一次请求的请求数据和响应数据。
    """
    request: RequestData
    response: ResponseData


class SessionData(BaseModel):
    """
    会话数据类，包含请求会话的数据，包括请求、响应、验证器和统计数据。
    """
    success: bool = False
    req_resps: List[ReqRespData] = []
    stat: RequestStat = RequestStat()
    address: AddressData = AddressData()
    validators: Dict = {}
