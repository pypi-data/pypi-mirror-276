# template.py
import json
from urllib.parse import urlparse

SETTINGS = '*** Settings ***\n'
TESTCASE = '*** Test Cases ***'
KEYWORDS = '*** Keywords ***\n'
ARGUMENTS = '[Arguments]'
TEMPLATE = '[Template]'
LIBRARY = 'Library'
TAG = 'Force Tags'
RESOURCE = 'Resource'

class RobotTemplate(object):

    def __init__(self):
        self.separate = ' ' * 4

    def make_settings(self):
        """组装settings部分"""
        settings_str = SETTINGS
        settings_str += TAG + self.separate + 'har2rf' + '\n'
        for library in ['RequestsLibrary', 'Collections', 'String', 'HttpLibrary.HTTP', '../../tools_library.py']:
            settings_str = settings_str + LIBRARY + self.separate + '{}\n'.format(library)
        settings_str += RESOURCE + self.separate + '../../../Public/https_request.txt' + '\n'
        return settings_str

    def make_testcase(self, url, method, queryString, postData):
        """组装testcase部分"""
        testcase_str = ""

        # 生成用例头部
        testcase_header = ""
        testcase_value = ""

        # 处理postData数据
        if postData:
            postData = json.loads(postData)
            if not postData:
                if not queryString:
                    testcase_header += '没有参数' + self.separate
                    testcase_value += 'Class_01' + self.separate
                else:
                    for query in queryString:
                        _value = query['value']
                        if not _value:
                            _value = '${EMPTY}'
                        testcase_header += query['name'] + self.separate
                        testcase_value += _value + self.separate

            if isinstance(postData, dict):
                for _header, _value in sorted(postData.items(), key=lambda x: x[0]):
                    if not _value:
                        _value = '${EMPTY}'
                    testcase_header += _header + self.separate
                    testcase_value += str(_value) + self.separate
            else:
                logging.warn('postData类型为:{}，不支持参数透传!'.format(type(postData)))
        else:
            if queryString:
                for query in queryString:
                    _value = query['value']
                    if not _value:
                        _value = '${EMPTY}'
                    testcase_header += query['name'] + self.separate
                    testcase_value += _value + self.separate
            else:
                testcase_header += '没有参数' + self.separate
                testcase_value += 'Class_01' + self.separate

        testcase_header = TESTCASE + self.separate + testcase_header

        # 生成用例内容
        testcase_name = 'Class_01'
        keyword_name = self.return_keyword_name(url, method)

        template_str = TEMPLATE + self.separate + keyword_name + '\n'

        testcase_str += testcase_header + '\n' + testcase_name + '\n' + self.separate
        testcase_str += template_str
        testcase_str += self.separate + testcase_value

        return testcase_str

    def make_keywords(self, url, method, headers, queryString, postData):
        """组装keyword部分"""
        keywords_str = ""
        keyword_name = self.return_keyword_name(url, method)

        # 组装关键字入参
        keyword_args = self.separate + ARGUMENTS + self.separate

        args = ""
        if postData:
            postData = json.loads(postData)
            if not postData:
                if not queryString:
                    args = args + '${%s}' % ('testcase') + self.separate
                else:
                    for query in queryString:
                        args = args + '${%s}' % (query['name']) + self.separate

            if isinstance(postData, dict):
                for _args, _value in sorted(postData.items(), key=lambda x: x[0]):
                    args = args + '${%s}' % (_args) + self.separate
        else:
            if not queryString:
                args = args + '${%s}' % ('testcase') + self.separate
            else:
                for query in queryString:
                    args = args + '${%s}' % (query['name']) + self.separate

        keyword_args += args
        keywords_str += KEYWORDS + keyword_name + '\n' + keyword_args

        # 组装关键字逻辑
        keyword_encoding = """
        Evaluate    reload(sys)    sys
        Evaluate    sys.setdefaultencoding( "utf-8" )    sys
        """
        keyword_path = """${path}=    set variable    """
        keyword_url = """${URL}=    set variable    """

        path = urlparse(url).path

        if method == 'POST':
            query_str = ""
            if queryString:
                for index, query in enumerate(queryString):
                    if len(queryString) > 1:
                        query_str = '{}={}'.format(query['name'], query['value'])
                        query_str += '&' + query_str
                    else:
                        query_str = '{}={}'.format(query['name'], query['value'])

            path = '{}?{}'.format(path, query_str)

        URL = urlparse(url).scheme + '://' + urlparse(url).netloc
        keyword_path += path
        keyword_path += '\n'
        keyword_url = self.separate * 2 + keyword_url + URL + '\n'

        keyword_datas = """${datas}=    create dictionary"""
        keyword_params = """${params}=    create dictionary"""
        keyword_datas = self.separate * 2 + keyword_datas
        keyword_params = '\n' + self.separate * 2 + keyword_params
        dict_datas = ""
        dict_params = ""

        if postData:
            if isinstance(postData, dict):
                for _args, _value in sorted(postData.items(), key=lambda x: x[0]):
                    dict_datas += """
            set to dictionary    ${datas}    %s=${%s}
                    """ % (_args, _args)

        if queryString and method == 'GET':
            for query in queryString:
                dict_params += """
        set to dictionary    ${params}    %s=${%s}
                        """ % (query['name'], query['name'])

        headers_datas = """${headers}=    create dictionary"""
        headers_datas = '\n' + self.separate * 2 + headers_datas
        headers_str = ""
        if headers:
            for header in headers:
                headers_str += """
        set to dictionary    ${headers}    %s=%s
                    """ % (header['name'], header['value'])

        if method == 'POST':
            request_method = '_Post_Request'
        elif method == 'GET':
            request_method = '_Get_Request'
        elif method == 'DELETE':
            request_method = '_Delete_Request'
        elif method == 'PUT':
            request_method = '_Put_Request'

        requests_str = """
        log    ${datas}
        log    ${headers}
        ${resp}=    %s    ${URL}    ${path}    ${datas}   ${params}    ${headers}
        log    ${resp.content}
        ${content}=    set variable    ${resp.content}
        ${content}=    charconver    ${resp.content}
        log json    ${content}      INFO
        should be true    ${resp.status_code}==200
        """ % (request_method)

        keywords_str = keywords_str + keyword_encoding + keyword_path + keyword_url + keyword_datas + \
                       dict_datas + keyword_params + dict_params + headers_datas + headers_str + requests_str
        return keywords_str

    def general_testcase(self, url, method, headers, queryString, postData):
        """生成RF用例"""
        robotfile = ""
        settings_str = self.make_settings()
        testcase_str = self.make_testcase(url, method, queryString, postData)
        keywords_str = self.make_keywords(url, method, headers, queryString, postData)
        robotfile += settings_str + '\n' + str(testcase_str) + '\n\n' + str(keywords_str)

        path = urlparse(url).path
        path_list = [els for els in path.split('/') if els]
        if len(path_list) <= 2:
            testsuite_name = '{}_{}.robot'.format(path_list[-1], method)
        else:
            testsuite_name = '{}_{}_{}.robot'.format(path_list[-2], path_list[-1], method)

        return testsuite_name, robotfile

    def return_keyword_name(self, url, method):
        '''返回关键字名称'''
        api_name = url.split('/')[-1].split('?')[0]
        keyword_name = '{}_{}_assertClass'.format(api_name, method)
        return keyword_name


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
from stp.http_requests import HttpSession
from stp.utils import *

class Test{class_name}(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.session = HttpSession()
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
        response = self.session.request('{method}', "{url}", params={params}, headers={headers}, data=json.dumps({datas}))
        logger.info(response)
        assert response.status_code == 200, '请求返回非200'
    """
    return testcase

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
from stp.http_requests import HttpSession
from stp.utils import *

@pytest.fixture(scope="class")
def session():
    session = HttpSession()
    return session

class Test{class_name}:
    url = "{url}"

    def setup_method(self):
        self.header = {headers}
        self.datas = {datas}
        self.params = {params}

    def teardown_method(self):
        pass

    def test_{method}_{class_name}(self, session):
        response = session.request('{method}', self.url, params=self.params, headers=self.header, data=json.dumps(self.datas))
        logger.info(response)
        assert response.status_code == 200, '请求返回非200'
    """
    return testcase

def render_template_robot(**kwargs):
    kwargs = kwargs.get('kwargs')
    class_name = kwargs.get("class_name")
    url = kwargs.get("url")
    headers = kwargs.get("headers")
    datas = eval(kwargs.get("datas"))
    params = kwargs.get("params")
    method = kwargs.get("method").lower()

    template = RobotTemplate()
    testsuite_name, robotfile = template.general_testcase(url, method, headers, params, datas)
    return robotfile
