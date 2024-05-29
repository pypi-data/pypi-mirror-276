# cli.py
# !/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse
import os
import sys
import yaml
import logging
from latp import __description__, __version__, __pro_name__
from latp import runner
from latp.case_generator.core import generate_testcases

logger = logging.getLogger(__name__)


def load_config(config_file):
    """
    加载配置文件。

    Args:
        config_file: 配置文件路径。

    Returns:
        配置字典。
    """
    if not os.path.exists(config_file):
        logger.warning(f"Config file {config_file} does not exist, using default config.yaml")
        config_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    """
    主函数，解析命令行参数并运行测试。
    """
    parser = argparse.ArgumentParser(prog=__pro_name__, description=__description__)
    parser.add_argument("-V", "--version", dest="version", action="store_true", help="show version")
    parser.add_argument("-k", default=None, action="store", help="run tests which match the given substring expression")
    parser.add_argument("-m", default=None, action="store", help="run tests with same marks")
    parser.add_argument("-c", "--config", default=None, action="store", help="path to config file")
    parser.add_argument("-co", "--collect-only", action="store_true", help="only collect testcase counts")
    parser.add_argument("--input-type", choices=["har", "swagger", "postman"], help="specify the input file type")
    parser.add_argument("--input-file", help="path to input file (HAR, Swagger JSON, Postman)")
    parser.add_argument("--output-type", choices=["unittest", "pytest", "robot"],
                        help="specify the output test case type")
    parser.add_argument("--output-dir", default=".", help="path to save generated test cases")
    parser.add_argument("path", nargs='?', help="please input test folder or module file", action="store")

    args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if args.input_file:
        if not args.input_type or not args.output_type:
            logger.error("生成测试用例需要指定 --input-type 和 --output-type 参数。")
            sys.exit(1)
        generate_testcases(args.input_file, args.input_type, args.output_dir, args.output_type)
        print(f"Test cases generated and saved to: {os.path.abspath(args.output_dir)}")
        sys.exit(0)

    config_path = args.config if args.config else 'config.yaml'
    config = load_config(config_path)

    test_path = args.path if args.path else config['tests']['test_path']

    if not test_path:
        logger.error("请提供测试文件夹路径，或者在配置文件中指定测试路径。")
        sys.exit(0)

    if not os.path.exists(test_path):
        logger.error(f'输入的路径不存在: {test_path}')
        sys.exit(0)

    if args.collect_only:
        # 统计测试用例数量
        test_case_count = runner.count_test_cases(test_path, config)
        print(f"总测试用例数量: {test_case_count}")
        sys.exit(0)

    if args.k:
        logger.info(f"测试路径: {test_path}")
        logger.info(f"用例过滤表达式: {args.k}")
    if args.m:
        logger.info(f"测试路径: {test_path}")
        logger.info(f"用例标签: {args.m}")

    runner.run(args, test_path, config)


if __name__ == "__main__":
    main()
