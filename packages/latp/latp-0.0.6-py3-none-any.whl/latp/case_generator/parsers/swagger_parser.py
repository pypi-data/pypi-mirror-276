# swagger_parser.py

from .base_parser import BaseParser
import json

from ..utils import camel


class SwaggerParser(BaseParser):
    def __init__(self, swagger_file_path):
        super().__init__(swagger_file_path)
        self.entries, self.version = self.load_swagger_entries(self.file_path)

    def load_swagger_entries(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            swagger_json = json.load(f)

        if "swagger" in swagger_json:
            version = "2.x"
        elif "openapi" in swagger_json:
            version = "3.x"
        else:
            raise ValueError("Unsupported Swagger/OpenAPI version")

        paths = swagger_json.get("paths", {})
        entries = []
        for path, methods in paths.items():
            for method, details in methods.items():
                if version == "2.x":
                    headers = {h["name"]: h.get("default", "") for h in details.get("parameters", []) if
                               h["in"] == "header"}
                    params = {p["name"]: p.get("default", "") for p in details.get("parameters", []) if
                              p["in"] == "query"}
                    body = {b["name"]: b.get("default", "") for b in details.get("parameters", []) if b["in"] == "body"}
                else:  # version == "3.x"
                    headers = {h["name"]: h.get("example", "") for h in details.get("parameters", []) if
                               h["in"] == "header"}
                    params = {p["name"]: p.get("example", "") for p in details.get("parameters", []) if
                              p["in"] == "query"}
                    body = details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("example",
                                                                                                             {})

                entry = {
                    "method": method.upper(),
                    "url": path,
                    "headers": headers,
                    "params": params,
                    "body": body
                }
                entries.append(entry)
        return entries, version

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
