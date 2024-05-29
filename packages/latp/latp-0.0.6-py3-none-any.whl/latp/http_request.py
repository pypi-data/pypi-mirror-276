# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu


import json
import time
import requests
import urllib3
from loguru import logger
from requests import Request, Response
from requests.exceptions import InvalidSchema, InvalidURL, MissingSchema, RequestException

from .base_request import BaseRequest
from .models import RequestData, ResponseData, SessionData, ReqRespData
from .utils import lower_dict_keys, omit_long_data

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiResponse(Response):
    """
    自定义响应类，扩展了 requests.Response 类，以便处理自定义错误。
    """

    def raise_for_status(self):
        if hasattr(self, "error") and self.error:
            raise self.error
        Response.raise_for_status(self)


def get_req_resp_record(resp_obj: Response):
    """
    从 Response 对象中获取请求和响应信息。

    Args:
        resp_obj: requests.Response 对象。

    Returns:
        ReqRespData 对象，包含请求和响应的详细信息。
    """

    def log_print(req_or_resp, r_type):
        msg = f"\n================== {r_type} details ==================\n"
        for key, value in req_or_resp.dict().items():
            if isinstance(value, dict) or isinstance(value, list):
                value = json.dumps(value, indent=4, ensure_ascii=False)
            msg += "{:<8} : {}\n".format(key, value)
        logger.debug(msg)

    request_headers = dict(resp_obj.request.headers)
    request_cookies = resp_obj.request._cookies.get_dict()
    request_body = resp_obj.request.body

    if request_body is not None:
        try:
            request_body = json.loads(request_body)
        except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
            pass

        request_content_type = lower_dict_keys(request_headers).get("content-type")
        if request_content_type and "multipart/form-data" in request_content_type:
            request_body = "upload file stream (OMITTED)"

    request_data = RequestData(
        method=resp_obj.request.method,
        url=resp_obj.request.url,
        headers=request_headers,
        cookies=request_cookies,
        body=request_body,
    )

    log_print(request_data, "request")

    resp_headers = dict(resp_obj.headers)
    lower_resp_headers = lower_dict_keys(resp_headers)
    content_type = lower_resp_headers.get("content-type", "")

    if "image" in content_type:
        response_body = resp_obj.content
    else:
        try:
            response_body = resp_obj.json()
        except ValueError:
            resp_text = resp_obj.text
            response_body = omit_long_data(resp_text)

    response_data = ResponseData(
        status_code=resp_obj.status_code,
        cookies=resp_obj.cookies or {},
        encoding=resp_obj.encoding,
        headers=resp_headers,
        content_type=content_type,
        body=response_body,
    )

    log_print(response_data, "response")

    req_resp_data = ReqRespData(request=request_data, response=response_data)
    return req_resp_data


class HttpRequest(BaseRequest):
    """
    HTTP 请求类，继承自 BaseRequest 类，实现具体的 HTTP 请求逻辑。
    """

    def __init__(self):
        self.session = requests.Session()
        self.data = SessionData()

    def send(self, method, url, **kwargs):
        """
        发送 HTTP 请求。

        Args:
            method: HTTP 方法，如 'GET'、'POST'。
            url: 请求的 URL。
            kwargs: 其他可选参数。

        Returns:
            requests.Response 对象。
        """
        self.data = SessionData()
        kwargs.setdefault("timeout", 120)
        kwargs["stream"] = True

        start_timestamp = time.time()
        response = self._send_request_safe_mode(method, url, **kwargs)
        response_time_ms = round((time.time() - start_timestamp) * 1000, 2)

        try:
            client_ip, client_port = response.raw._connection.sock.getsockname()
            self.data.address.client_ip = client_ip
            self.data.address.client_port = client_port
            logger.debug(f"client IP: {client_ip}, Port: {client_port}")
        except Exception:
            pass

        try:
            server_ip, server_port = response.raw._connection.sock.getpeername()
            self.data.address.server_ip = server_ip
            self.data.address.server_port = server_port
            logger.debug(f"server IP: {server_ip}, Port: {server_port}")
        except Exception:
            pass

        content_size = int(dict(response.headers).get("content-length") or 0)
        self.data.stat.response_time_ms = response_time_ms
        self.data.stat.elapsed_ms = response.elapsed.microseconds / 1000.0
        self.data.stat.content_size = content_size

        response_list = response.history + [response]
        self.data.req_resps = [get_req_resp_record(resp_obj) for resp_obj in response_list]

        try:
            response.raise_for_status()
        except RequestException as ex:
            logger.error(f"{str(ex)}")
        else:
            logger.info(
                f"status_code: {response.status_code}, "
                f"response_time(ms): {response_time_ms} ms, "
                f"response_length: {content_size} bytes"
            )

        return response

    def _send_request_safe_mode(self, method, url, **kwargs):
        """
        安全模式发送 HTTP 请求，并捕获可能出现的连接问题异常。

        Args:
            method: HTTP 方法。
            url: 请求的 URL。
            kwargs: 其他可选参数。

        Returns:
            requests.Response 对象，或 ApiResponse 对象（用于处理异常情况）。
        """
        try:
            return self.session.request(method, url, **kwargs)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except RequestException as ex:
            resp = ApiResponse()
            resp.error = ex
            resp.status_code = 0
            resp.request = Request(method, url).prepare()
            return resp
