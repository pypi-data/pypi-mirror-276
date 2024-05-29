# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu
# @file    : __init__.py
# @time    : 2024/5/24 下午15:46


import logging
import yaml
import os

# 包信息管理
__description__ = "A custom testing framework based on pytest"
__version__ = "0.0.5"
__pro_name__ = "latp"


def configure_logging(config_file='config.yaml'):
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logging_config = config.get('logging', {})
        log_level = logging_config.get('level', 'INFO').upper()
        log_file = logging_config.get('file', 'app.log')
        log_format = logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logging.basicConfig(level=log_level, format=log_format, filename=log_file, encoding='utf-8', filemode='w')
        console = logging.StreamHandler()
        console.setLevel(log_level)
        formatter = logging.Formatter(log_format)
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


configure_logging()
