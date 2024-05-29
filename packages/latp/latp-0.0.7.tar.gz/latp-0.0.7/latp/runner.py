# runner.py
# !/usr/bin/python3
# -*- coding: utf-8 -*-
import inspect
import os
import sys
import glob
import pytest
import importlib.util
import logging
import re

logger = logging.getLogger(__name__)


def find_modules_from_folder(folder, module_pattern):
    """
    从指定文件夹中查找符合模式的模块。

    Args:
        folder: 文件夹路径。
        module_pattern: 模块名称匹配模式（正则表达式）。

    Returns:
        模块名称和路径的列表。
    """
    absolute_f = os.path.abspath(folder)
    modules = glob.glob(os.path.join(absolute_f, "**", "*.py"), recursive=True)
    pattern = re.compile(module_pattern)
    return [(os.path.relpath(f, start=absolute_f)[:-3].replace(os.sep, '.'), f) for f in modules if
            os.path.isfile(f) and not f.endswith('__init__.py') and pattern.match(os.path.basename(f)[:-3])]


def import_modules_dynamically(module, file_path):
    """
    动态导入模块。

    Args:
        module: 模块名称。
        file_path: 文件路径。

    Returns:
        导入的模块对象。
    """
    spec = importlib.util.spec_from_file_location(module, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def collect_test_cases(_module, test_case_set, module_file, class_pattern, function_pattern):
    """
    收集测试用例。

    Args:
        _module: 导入的模块对象。
        test_case_set: 测试用例集合。
        module_file: 模块文件路径。
        class_pattern: 类匹配模式（正则表达式）。
        function_pattern: 函数/方法匹配模式（正则表达式）。
    """
    module_file_path = os.path.relpath(module_file)
    class_re = re.compile(class_pattern)
    function_re = re.compile(function_pattern)

    for func_name, func in inspect.getmembers(_module, inspect.isfunction):
        if function_re.match(func_name):
            test_case = f"{module_file_path}::{func_name}"
            test_case_set.add((test_case, func))

    for cls_name, cls in inspect.getmembers(_module, inspect.isclass):
        if class_re.match(cls_name):
            for func_name, func in inspect.getmembers(cls, inspect.isfunction):
                if function_re.match(func_name):
                    test_case = f"{module_file_path}::{cls_name}::{func_name}"
                    test_case_set.add((test_case, func))


def filter_test_cases(test_case_set, keyword, mark):
    """
    过滤测试用例。

    Args:
        test_case_set: 测试用例集合。
        keyword: 关键字过滤表达式。
        mark: 标记过滤表达式。

    Returns:
        过滤后的测试用例集合。
    """
    filtered_cases = set()

    for test_case, func in test_case_set:
        if keyword and keyword not in test_case:
            continue
        if mark:
            func_marks = getattr(func, "__test_case_mark__", [])
            if not isinstance(func_marks, list):
                func_marks = [func_marks]
            if mark not in func_marks:
                continue
        filtered_cases.add(test_case)

    return filtered_cases


def run_test_case(test_case_set):
    """
    运行测试用例。

    Args:
        test_case_set: 测试用例集合。

    Returns:
        pytest 的运行结果。
    """
    logger.info(f"本次执行用例的数量为: {len(test_case_set)}")
    extra_args_list = ["-vs", "--tb=short"] + list(test_case_set)
    logger.info(f"运行的参数列表：{extra_args_list}")
    return pytest.main(extra_args_list)


def get_test_cases(test_path, config):
    """
    获取所有测试用例。

    Args:
        test_path: 测试路径。
        config: 配置字典。

    Returns:
        测试用例集合。
    """
    if os.path.isfile(test_path):
        # 单个文件模式
        module_list = [(os.path.splitext(os.path.basename(test_path))[0], test_path)]
    else:
        # 文件夹模式
        module_list = find_modules_from_folder(test_path, config['tests']['module_pattern'])

    test_case_set = set()
    for module in module_list:
        module_name, module_file = module
        _module = import_modules_dynamically(module_name, module_file)
        collect_test_cases(_module, test_case_set, module_file, config['tests']['class_pattern'],
                           config['tests']['function_pattern'])

    return test_case_set


def run(args, test_path, config):
    """
    运行测试。

    Args:
        args: 命令行参数。
        test_path: 测试路径。
        config: 配置字典。
    """
    logger.info(f"测试路径: {test_path}")

    keyword = args.k if args.k is not None else config['tests']['keyword_expression']
    mark = args.m if args.m is not None else config['tests']['mark_expression']

    logger.info(f"关键字过滤表达式: {keyword}")
    logger.info(f"标记过滤表达式: {mark}")

    try:
        test_case_set = get_test_cases(test_path, config)
    except Exception as e:
        logger.error(f"Failed to get test cases: {e}")
        sys.exit(1)

    logger.info(f"所有找到的测试用例: {test_case_set}")

    filtered_test_cases = filter_test_cases(test_case_set, keyword, mark)

    if filtered_test_cases:
        logger.info(f"过滤后的测试用例: {filtered_test_cases}")
        sys.exit(run_test_case(filtered_test_cases))
    else:
        logger.info("未找到任何匹配的测试用例。")


def count_test_cases(test_path, config):
    """
    统计测试用例数量。

    Args:
        test_path: 测试用例路径。
        config: 配置字典。

    Returns:
        测试用例数量。
    """
    try:
        test_case_set = get_test_cases(test_path, config)
        return len(test_case_set)
    except Exception as e:
        logger.error(f"Failed to count test cases: {e}")
        return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test Runner")
    parser.add_argument('test_path', type=str, help="Path to the test files or directory")
    parser.add_argument('-k', type=str, help="Only run tests that match the given substring expression")
    parser.add_argument('-m', type=str, help="Only run tests that have the given mark expression")
    parser.add_argument('-c', '--config', type=str, default='config.yaml', help="Path to the config file")
    parser.add_argument('-co', '--collect-only', action='store_true', help="Only collect testcase counts")
    args = parser.parse_args()

    from cli import load_config  # 从 cli 模块中导入 load_config 函数

    config_path = args.config if args.config else 'config.yaml'
    config = load_config(config_path)

    if args.collect_only:
        count = count_test_cases(args.test_path, config)
        print(f"Total test cases: {count}")
    else:
        run(args, args.test_path, config)
