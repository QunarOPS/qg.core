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
#


class Singleton(object):
    __instance = None

    def __new__(classtype, *args, **kwargs):
        if classtype != type(classtype.__instance):
            classtype.__instance = object.__new__(classtype, *args, **kwargs)
            classtype.__instance.init_singleton()

        return classtype.__instance

    def init_singleton(self):
        pass
