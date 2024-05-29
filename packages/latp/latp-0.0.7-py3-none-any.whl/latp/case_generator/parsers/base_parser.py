# base_parser.py

class BaseParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def fetch_request_response(self):
        raise NotImplementedError("fetch_request_response must be implemented in subclasses")

    def parse_request(self, req_obj):
        raise NotImplementedError("parse_request must be implemented in subclasses")
