# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu

""" 自定义异常类模块，用于标记测试中的错误类型 """


class MyBaseFailure(Exception):
    """
    基础失败异常类。
    """
    pass


class ValidationFailure(MyBaseFailure):
    """
    验证失败异常类。
    """
    pass


class MyBaseError(Exception):
    """
    基础错误异常类。
    """
    pass


class FileFormatError(MyBaseError):
    """
    文件格式错误异常类。
    """
    pass


class TestCaseFormatError(FileFormatError):
    """
    测试用例格式错误异常类。
    """
    pass


class TestSuiteFormatError(FileFormatError):
    """
    测试套件格式错误异常类。
    """
    pass


class ParamsError(MyBaseError):
    """
    参数错误异常类。
    """
    pass


class NotFoundError(MyBaseError):
    """
    未找到错误异常类。
    """
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    """
    文件未找到异常类。
    """
    pass


class FunctionNotFound(NotFoundError):
    """
    函数未找到异常类。
    """
    pass


class VariableNotFound(NotFoundError):
    """
    变量未找到异常类。
    """
    pass


class EnvNotFound(NotFoundError):
    """
    环境变量未找到异常类。
    """
    pass


class ApiNotFound(NotFoundError):
    """
    API 未找到异常类。
    """
    pass


class TestcaseNotFound(NotFoundError):
    """
    测试用例未找到异常类。
    """
    pass
