# postman_parser.py

from .base_parser import BaseParser
import json

from ..utils import camel


class PostmanParser(BaseParser):
    def __init__(self, postman_file_path):
        super().__init__(postman_file_path)
        self.entries = self.load_postman_entries(self.file_path)

    def load_postman_entries(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            postman_json = json.load(f)

        items = postman_json.get("item", [])
        entries = []
        for item in items:
            request = item.get("request", {})
            method = request.get("method", "").upper()
            url = request.get("url", {}).get("raw", "")
            headers = {h["key"]: h.get("value", "") for h in request.get("header", [])}
            params = {p["key"]: p.get("value", "") for p in request.get("url", {}).get("query", [])}
            body = request.get("body", {}).get("raw", {})

            entry = {"method": method, "url": url, "headers": headers, "params": params, "body": body}
            entries.append(entry)
        return entries

    def fetch_request_response(self):
        datas_dict = {}
        for index, item in enumerate(self.entries):
            datas_dict[index + 1] = {"request": item}
        return datas_dict

    def parse_request(self, req_obj):
        if isinstance(req_obj, dict):
            method = req_obj.get("method")
            url = req_obj.get("url")
            headers = req_obj.get("headers")
            datas = json.dumps(req_obj.get("body", {}))
            params = req_obj.get("params")
            class_name = camel(url.split('/')[-1])
            if class_name.isdigit():
                class_name = camel(url.split('/')[-2])
            return {"method": method, "url": url, "headers": headers, "datas": datas, "class_name": class_name,
                    "params": params}
        else:
            raise ValueError("Request object must be a dictionary")
