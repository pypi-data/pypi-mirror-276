# utils.py
import io
import json
import logging
import sys
import pathlib
import yaml
from re import sub

logger = logging.getLogger(__name__)


def load_har_log_entries(file_path):
    try:
        with io.open(file_path, "r+", encoding="utf-8-sig") as f:
            content_json = json.loads(f.read())
            return content_json["log"]["entries"]
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        logger.error(f"HAR file content error: {file_path}, error: {e}")
        sys.exit(1)


def x_www_form_urlencoded(post_data):
    try:
        if isinstance(post_data, dict):
            return "&".join([
                u"{}={}".format(key, value)
                for key, value in post_data.items()
            ])
        else:
            return post_data
    except Exception as e:
        logger.error(f"Error in x_www_form_urlencoded: {e}")
        return post_data


def convert_list_to_dict(origin_list):
    try:
        return {
            item["name"]: item.get("value")
            for item in origin_list
        }
    except Exception as e:
        logger.error(f"Error in convert_list_to_dict: {e}")
        return {}


def fetch_yaml(yaml_file):
    try:
        with io.open(pathlib.Path(yaml_file), 'r', encoding="utf-8") as datas:
            return yaml.load(datas, Loader=yaml.FullLoader)
    except yaml.YAMLError as e:
        logger.error(f"Error loading YAML file {yaml_file}: {e}")
        return {}


def camel(_str):
    s = sub(r"(_|-)+", " ", _str).title().replace(" ", "")
    return s[0].lower() + s[1:]
