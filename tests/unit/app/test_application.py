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
# Author: jaypei <jaypei97159@gmail.com>
#


import mock
from testtools import TestCase
from testtools.matchers import Equals, Not, Is

from qg.core.app import QApplication


class TestQApplication(TestCase):

    def test_singleton(self):
        class TestApplication1(QApplication):
            name = "test1"
            version = "0"

        class TestApplication2(QApplication):
            name = "test2"
            version = "0"

        t1 = TestApplication1()
        t2 = TestApplication2()
        self.assertThat(t1, Is(TestApplication1()))
        self.assertThat(t2, Is(TestApplication2()))
        self.assertThat(t1, Not(Is(t2)))

    def test_app_members(self):

        class TestApplication1(QApplication):
            name = "test-application"
            version = "100.0.1"

        t1 = TestApplication1()
        self.assertThat(t1.name, Equals("test-application"))
        self.assertThat(t1.version, Equals("100.0.1"))

    def test_app_run(self):

        class TestApplication1(QApplication):
            name = "test-application1"
            version = "0"

        class TestApplication2(QApplication):
            name = "test-application2"
            version = "0"

            def run(self):
                pass

        with mock.patch('oslo_config.cfg.CONF') as instance:
            instance.return_value = True
            t1 = TestApplication1()
            self.assertRaises(NotImplementedError,
                              t1.main)
            t2 = TestApplication2()
            t2.main()

    def test_life_cycle(self):

        class TestApplication1(QApplication):
            name = "test-application1"
            version = "0"

            def run(self):
                pass

        t1 = TestApplication1()
        t1.init_app = mock.MagicMock()
        t1.configure = mock.MagicMock()
        t1.run = mock.MagicMock()
        t1.shutdown = mock.MagicMock()
        t1.main()
        # TODO(jaypei): 如何测试init_app阶段？
        # t1.init_app.assert_called_once_with()
        t1.configure.assert_called_once_with()
        t1.run.assert_called_once_with()
        t1.shutdown.assert_called_once_with()
