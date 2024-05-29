# !/usr/bin/python3
# -*- coding: utf-8 -*-
import inspect
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class TestMark(object):
    """
    用于给测试类或测试方法添加标记属性的装饰器类。
    """
    def __init__(self, mark=None):
        """
        初始化标记。
        :param mark: 标记名称
        """
        self.mark = mark

    def __call__(self, obj):
        """
        为类或方法添加标记属性。
        :param obj: 类或方法
        :return: 带有标记属性的类或方法
        """
        if inspect.isclass(obj):
            self._add_mark_to_class(obj)
        else:
            obj = self._add_mark_to_method(obj)
        return obj

    def _add_mark_to_class(self, cls):
        """
        为类及其方法添加标记属性。
        :param cls: 类对象
        """
        logger.info(f"Adding mark '{self.mark}' to class '{cls.__name__}' and its methods.")
        setattr(cls, "__test_case_mark__", self.mark)
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            if name.startswith('test') or name.endswith('test'):
                self._add_mark_to_method(method)

    def _add_mark_to_method(self, method):
        """
        为方法添加标记属性。
        :param method: 方法对象
        :return: 带有标记属性的方法对象
        """
        logger.info(f"Adding mark '{self.mark}' to method '{method.__name__}'.")
        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)

        existing_marks = getattr(method, "__test_case_mark__", [])
        if not isinstance(existing_marks, list):
            existing_marks = [existing_marks]
        existing_marks.append(self.mark)
        setattr(wrapper, "__test_case_mark__", existing_marks)
        return wrapper

# 示例用法
# @TestMark(mark="example_class_mark")
# class TestExample:
#     def test_method1(self):
#         pass
#
#     @TestMark(mark="example_method_mark")
#     def test_method2(self):
#         pass

# TestExample 类现在拥有 __test_case_mark__ 属性
# TestExample.test_method1 方法现在拥有 __test_case_mark__ 属性 (继承自类的标记)
# TestExample.test_method2 方法现在拥有 __test_case_mark__ 属性 (继承自类的标记以及自己定义的标记)
