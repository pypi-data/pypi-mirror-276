# core.py
# coding=utf-8
from latp.case_generator.utils import camel
from latp.case_generator.templates import render_template_unittest, render_template_pytest, render_template_robot
from latp.case_generator.parsers.har_parser import HarParser
from latp.case_generator.parsers.swagger_parser import SwaggerParser
from latp.case_generator.parsers.postman_parser import PostmanParser
import os
import logging

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

logger = logging.getLogger(__name__)


def generate_testcases(input_file, input_type, output_dir, output_type):
    try:
        if input_type == "har":
            parser = HarParser(input_file)
        elif input_type == "swagger":
            parser = SwaggerParser(input_file)
        elif input_type == "postman":
            parser = PostmanParser(input_file)
        else:
            logger.error(f"Unsupported input type: {input_type}")
            raise ValueError("Unsupported input type")

        datas_dict = parser.fetch_request_response()

        for key, obj in datas_dict.items():
            try:
                datas = parser.parse_request(obj)
            except Exception as e:
                logger.error(f"Failed to parse request object: {e}")
                continue

            if output_type == "pytest":
                testcase_template = render_template_pytest(kwargs=datas)
                extension = ".py"
            elif output_type == "unittest":
                testcase_template = render_template_unittest(kwargs=datas)
                extension = ".py"
            elif output_type == "robot":
                testcase_template = render_template_robot(kwargs=datas)
                extension = ".robot"
            else:
                logger.error(f"Unsupported output type: {output_type}")
                raise ValueError("Unsupported output type")

            class_name = datas.get('class_name')
            method = datas.get("method").lower()
            path = os.path.join(output_dir, f"test_{method}_{class_name}{extension}")

            if not os.path.exists(output_dir):
                logger.info(f"Creating output directory: {output_dir}")
                os.makedirs(output_dir)

            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(testcase_template)
                logger.info(f"Test case generated: {path}")
            except Exception as e:
                logger.error(f"Failed to write test case to file {path}: {e}")

    except Exception as e:
        logger.error(f"Failed to generate test cases: {e}")
        raise


# 示例使用方法
if __name__ == "__main__":
    generate_testcases("example.har", "har", "./output", "pytest")
