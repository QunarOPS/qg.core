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

from qg.core import gettextutils
gettextutils.install('testing', lazy=True)

from oslo_config import cfg
from testtools import TestCase
import os

CONF = cfg.CONF


class TestGettext(TestCase):

    def setUp(self):
        # TODO(jianingy): 自动设置境变量 TESTING_LOCALEDIR, 测试用例里 locale
        #                 用中文
        localedir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', 'locale'))
        cmd = ("msgfmt -o %s/zh_CN/LC_MESSAGES/testing.mo "
               "%s/zh_CN/LC_MESSAGES/testing.po") % (localedir, localedir)
        os.system(cmd)
        os.environ['TESTING_LOCALEDIR'] = localedir
        os.environ['LC_ALL'] = 'zh_CN.UTF-8'
        CONF.set_default('domain', 'testing', 'i18n')
        super(TestGettext, self).setUp()

    def test_gettext_without_translation(self):
        self.assertEqual(_('Hello'), 'Hello')

    def test_gettext_with_translation(self):
        self.assertEqual(_('Hello, world'), u'世界你好')
