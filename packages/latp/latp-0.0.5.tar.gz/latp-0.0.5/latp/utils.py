# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu

# utils.py
# !/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import random
import string
import time
import collections
import json
import os
import platform
import sys
from loguru import logger

from .exceptions import ParamsError
from . import __version__, exceptions

LOGGER_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <level>{message}</level>"


def init_logger():
    """
    初始化日志记录器，设置日志格式和级别。
    """
    logger.remove()
    logger.add(sys.stderr, format=LOGGER_FORMAT, level="INFO")


def gen_random_string(str_len):
    """
    生成指定长度的随机字符串。

    Args:
        str_len: 字符串长度。

    Returns:
        随机字符串。
    """
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(str_len))


def get_timestamp(str_len=13):
    """
    获取时间戳字符串，长度介于 0 到 16 之间。

    Args:
        str_len: 时间戳字符串长度。

    Returns:
        时间戳字符串。

    Raises:
        ParamsError: 如果长度不在 0 到 16 之间，抛出参数错误。
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]
    raise ParamsError("timestamp length can only between 0 and 16.")


def get_current_date(fmt="%Y-%m-%d"):
    """
    获取当前日期字符串，默认格式为 %Y-%m-%d。

    Args:
        fmt: 日期格式。

    Returns:
        当前日期字符串。
    """
    return datetime.datetime.now().strftime(fmt)


def set_os_environ(variables_mapping):
    """
    设置环境变量。

    Args:
        variables_mapping: 环境变量映射。
    """
    for variable in variables_mapping:
        os.environ[variable] = variables_mapping[variable]
        logger.debug(f"Set OS environment variable: {variable}")


def unset_os_environ(variables_mapping):
    """
    取消设置环境变量。

    Args:
        variables_mapping: 环境变量映射。
    """
    for variable in variables_mapping:
        os.environ.pop(variable)
        logger.debug(f"Unset OS environment variable: {variable}")


def get_os_environ(variable_name):
    """
    获取环境变量的值。

    Args:
        variable_name: 环境变量名称。

    Returns:
        环境变量的值。

    Raises:
        EnvNotFound: 如果环境变量未找到，抛出异常。
    """
    try:
        return os.environ[variable_name]
    except KeyError:
        raise exceptions.EnvNotFound(variable_name)


def omit_long_data(body, omit_len=512):
    """
    省略过长的字符串或字节数据。

    Args:
        body: 字符串或字节数据。
        omit_len: 省略的长度。

    Returns:
        省略后的数据。
    """
    if not isinstance(body, (str, bytes)):
        return body

    body_len = len(body)
    if body_len <= omit_len:
        return body

    omitted_body = body[:omit_len]
    appendix_str = f" ... OMITTED {body_len - omit_len} CHARACTORS ..."
    if isinstance(body, bytes):
        appendix_str = appendix_str.encode("utf-8")

    return omitted_body + appendix_str


def lower_dict_keys(origin_dict):
    """
    将字典中的键转换为小写。

    Args:
        origin_dict: 原始字典。

    Returns:
        键全部小写的字典。
    """
    if not origin_dict or not isinstance(origin_dict, dict):
        return origin_dict
    return {key.lower(): value for key, value in origin_dict.items()}


def print_info(info_mapping):
    """
    打印映射信息。

    Args:
        info_mapping: 输入（变量）或输出映射。
    """
    if not info_mapping:
        return

    content_format = "{:<16} : {:<}\n"
    content = "\n==================== Output ====================\n"
    content += content_format.format("Variable", "Value")
    content += content_format.format("-" * 16, "-" * 29)

    for key, value in info_mapping.items():
        if isinstance(value, (tuple, collections.deque)):
            continue
        elif isinstance(value, (dict, list)):
            value = json.dumps(value)
        elif value is None:
            value = "None"

        content += content_format.format(key, value)

    content += "-" * 48 + "\n"
    logger.info(content.encode('utf-8').decode("unicode_escape"))


def print_testcase_list(testcase_list):
    """
    打印测试用例列表。

    Args:
        testcase_list: 测试用例列表。
    """
    if not testcase_list:
        return

    content_format = "{:<16} : {:<}\n"
    content = "\n==================== Output ====================\n"
    content += content_format.format("用例序号", "用例名称")
    content += content_format.format("-" * 16, "-" * 29)

    for index, item in enumerate(testcase_list):
        index = f"用例编号：{index + 1}"
        content += content_format.format(index, item)

    content += "-" * 48 + "\n"
    logger.info(content)
    logger.info(f"用例总数为:{len(testcase_list)}")
    logger.info("\n==================== End ====================\n")


def get_platform():
    """
    获取平台信息，包括 HttpRunner 版本、Python 版本和操作系统平台。

    Returns:
        平台信息字典。
    """
    return {
        "httprunner_version": __version__,
        "python_version": "{} {}".format(platform.python_implementation(), platform.python_version()),
        "platform": platform.platform(),
    }
