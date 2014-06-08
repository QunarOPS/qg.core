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
from testtools.matchers import Equals

from qg.core.app import QApplication
from qg.core.app import QExtension


class TestApplication1(QApplication):
    name = 'test-application1'
    version = '0'

    def create(self):
        super(TestApplication1, self).create()
        self.register_extension(Extension1())
        self.register_extension(Extension2(i=100))
        self.msg_trace = []

    def init_app(self):
        super(TestApplication1, self).init_app()
        self.msg_trace.append("init_app()")

    def configure(self):
        super(TestApplication1, self).configure()
        self.msg_trace.append("configure()")

    def run(self):
        self.msg_trace.append("run()")

    def shutdown(self):
        super(TestApplication1, self).shutdown()
        self.msg_trace.append("shutdown()")


class Extension1(QExtension):

    name = "Extension1"

    def pre_init_app(self, evt, app):
        app.msg_trace.append("Extension1.pre_init_app()")

    def post_init_app(self, evt, app, rlt):
        app.msg_trace.append("Extension1.post_init_app()")

    def pre_configure(self, evt, app):
        app.msg_trace.append("Extension1.pre_configure()")

    def post_configure(self, evt, app, rlt):
        app.msg_trace.append("Extension1.post_configure()")

    def pre_run(self, evt, app):
        app.msg_trace.append("Extension1.pre_run()")

    def post_run(self, evt, app, rlt):
        app.msg_trace.append("Extension1.post_run()")

    def pre_shutdown(self, evt, app):
        app.msg_trace.append("Extension1.pre_shutdown()")

    def post_shutdown(self, evt, app, rlt):
        app.msg_trace.append("Extension1.post_shutdown()")


class Extension2(QExtension):

    name = "Extension2"

    def __init__(self, i):
        self.i = i

    def post_init_app(self, evt, app, rlt):
        app.msg_trace.append("Extension2.post_init_app(),i=%d" %
                             self.i)


class TestQExtension(TestCase):

    def test_extension(self):

        t1 = TestApplication1()
        with mock.patch('sys.argv', ['test']):
            t1.main()
        self.assertThat(t1.msg_trace, Equals([
            'Extension1.pre_init_app()',
            'init_app()',
            'Extension1.post_init_app()',
            'Extension2.post_init_app(),i=100',
            'Extension1.pre_configure()',
            'configure()',
            'Extension1.post_configure()',
            'Extension1.pre_run()',
            'run()',
            'Extension1.post_run()',
            'Extension1.pre_shutdown()',
            'shutdown()',
            'Extension1.post_shutdown()'
        ]))
