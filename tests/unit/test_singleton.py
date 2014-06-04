# -*- coding: utf-8 -*-
#
# Copyright 2014, Qunar OPSDEV
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


from testtools import TestCase
from testtools.matchers import Equals, Not, Is

from qg.core.singleton import Singleton


class TestSingleton(TestCase):

    def test_one_object(self):

        class Cls1(Singleton):
            pass

        class Cls2(Singleton):
            pass

        t1 = Cls1()
        t2 = Cls2()
        self.assertThat(t1, Is(Cls1()))
        self.assertThat(t2, Is(Cls2()))
        self.assertThat(t1, Not(Is(t2)))

    def test_init(self):

        class Cls1(Singleton):
            def init_singleton(self):
                self.cnt = 100

            def inc(self):
                self.cnt += 1
                return self.cnt

        t1 = Cls1()
        self.assertThat(t1.cnt, Equals(100))
        t1.inc()
        self.assertThat(t1.cnt, Equals(101))
        self.assertThat(Cls1().inc(), Equals(102))
