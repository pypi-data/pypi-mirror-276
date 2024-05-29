# unittest_template.py
def render_template_unittest(**kwargs):
    kwargs = kwargs.get('kwargs')
    class_name = kwargs.get("class_name")
    url = kwargs.get("url")
    headers = kwargs.get("headers")
    datas = eval(kwargs.get("datas"))
    params = kwargs.get("params")
    method = kwargs.get("method").lower()

    testcase = f"""
#coding=utf-8
import unittest
from latp.request import RequestManager
from latp.utils import *

class Test{class_name}(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = RequestManager()
        cls.url = "{url}"


    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.header = {headers}
        self.datas = {datas}
        self.params = {params}

    def tearDown(self) -> None:
        pass

    def test_{method}_{class_name}(self):
        response = self.manager.send_http('{method}', "{url}", params={params}, headers={headers}, data=json.dumps({datas}))
        logger.info(response)
        self.assertEqual(response.status_code, 200, '请求返回非200')
    """
    return testcase
