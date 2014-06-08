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
# Author: Jianing Yang <jianingy.yang@gmail.com>
#
from testtools import TestCase

import logging
import mock

from qg.core.app.application import QApplication
from qg.core.app.exts.log import QLogExtension
from qg.core import log

LOG = log.getLogger(__name__)


class TestApplication(QApplication):
    name = 'test-application1'
    version = '0'

    def create(self):
        super(TestApplication, self).create()
        self.register_extension(QLogExtension())

    def init_app(self):
        LOG.warn('hello')
        super(TestApplication, self).init_app()

    def run(self):
        pass


class TestLogExtension(TestCase):

    def test_create_log_extension(self):
        with mock.patch('qg.core.log.setup') as instance:
            app = TestApplication()
            with mock.patch('sys.argv', ['test']):
                app.main()
                instance.assert_called_once_with('test-application1')

    def test_set_log_level(self):
        app = TestApplication()
        with mock.patch('sys.argv', ['test', '--debug']):
            app.main()
            self.assertEqual(LOG.logger.getEffectiveLevel(), logging.DEBUG)
