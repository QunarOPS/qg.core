# -*- coding: utf-8 -*-
#
# Copyright 2013, Qunar OPSDEV
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# Author: zhen.pei <zhen.pei@qunar.com>
# Author: Jianing Yang <jianing.yang@qunar.com>
#

from testtools import TestCase

from qg.core.exception import QException


class FormatException(QException):
    message = "Exception Message: %(reason)s"


class PlainException(QException):
    pass


class NormalException(QException):
    message = 'normal'


def raise_format_exception():
    raise FormatException(reason='sample message')


def raise_plain_exception():
    raise PlainException(message='sample message')


class TestException(TestCase):

    def test_format_exception(self):
        # NOTE(jianingy): 如果传入非 message 变量 __str__ 应该用 message 内容做
        # 格式化
        self.assertRaises(FormatException, raise_format_exception)
        try:
            raise_format_exception()
        except FormatException as e:
            self.assertEqual(str(e), 'Exception Message: sample message')

    def test_plain_exception(self):
        # NOTE(jianingy): 如果传入 message 变量 __str__ 应该直接显示 message 内
        # 容
        self.assertRaises(PlainException, raise_plain_exception)
        try:
            raise_plain_exception()
        except PlainException as e:
            self.assertEqual(str(e), 'sample message')

    def test_normal_exception(self):
        e = NormalException('special')
        self.assertEqual(e.message, 'special')
