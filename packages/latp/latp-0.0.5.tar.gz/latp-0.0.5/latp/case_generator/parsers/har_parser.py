# har_parser.py

from .base_parser import BaseParser
from ..utils import load_har_log_entries, camel


class HarParser(BaseParser):
    def __init__(self, har_file_path):
        super().__init__(har_file_path)
        self.entries = load_har_log_entries(self.file_path)

    def fetch_request_response(self):
        datas_dict = {}
        for index, item in enumerate(self.entries):
            datas_dict[index + 1] = {"request": item.get("request"), "response": item.get('response')}
        return datas_dict

    def parse_request(self, req_obj):
        if isinstance(req_obj, dict):
            method = req_obj.get("request").get("method")
            url = req_obj.get("request").get("url")
            headers = {item.get("name"): item.get("value") for item in req_obj.get("request").get("headers", [])}
            datas = req_obj.get("request").get("postData", {}).get("text", "")
            params = req_obj.get("request").get("queryString", [])
            class_name = camel(url.split('/')[-1])
            if class_name.isdigit():
                class_name = camel(url.split('/')[-2])
            return {"method": method, "url": url, "headers": headers, "datas": datas, "class_name": class_name,
                    "params": params}
        else:
            raise ValueError("Request object must be a dictionary")
