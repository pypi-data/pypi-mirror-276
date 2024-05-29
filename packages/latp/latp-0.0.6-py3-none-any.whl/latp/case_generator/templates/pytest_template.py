# pytest_template.py
def render_template_pytest(**kwargs):
    kwargs = kwargs.get('kwargs')
    class_name = kwargs.get("class_name")
    url = kwargs.get("url")
    headers = kwargs.get("headers")
    datas = eval(kwargs.get("datas"))
    params = kwargs.get("params")
    method = kwargs.get("method").lower()

    testcase = f"""
#coding=utf-8
import pytest
from latp.request import RequestManager
from latp.utils import *

class Test{class_name}:
    @classmethod
    def setup_class(cls):
        cls.manager = RequestManager()
        cls.url = "{url}"

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        self.header = {headers}
        self.datas = {datas}
        self.params = {params}

    def teardown_method(self):
        pass

    def test_{method}_{class_name}(self):
        response = self.manager.send_http('{method}', "{url}", params={params}, headers={headers}, data=json.dumps({datas}))
        logger.info(response)
        assert response.status_code == 200, '请求返回非200'
    """
    return testcase
