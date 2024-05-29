# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : Tanyu
# @file    : test_latp1.py
# @time    : 2024/5/24 下午15:46

import pytest

from latp.decorators import TestMark


class Login:
    @staticmethod
    def login_user(username, password):
        # 这里写你的业务逻辑，简单起见，我返回True
        print('\n%s' % username)
        print('\n%s' % password)
        return True


@TestMark("smoke3")
class TestLogin:
    def test_login(self):
        username = 'test_username'
        password = 'test_password'
        print('测试用例1')
        assert Login.login_user(username, password) == True

    @TestMark("smoke1")
    @TestMark("smoke2")
    def test_demo1(self):
        print('测试用例2')
        assert True

    def test_demo2(self):
        print('测试用例3')
        assert False
