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


from qg.core.exception import QException


class ObservableError(QException):
    message = "Observable error occered."


class Event(object):
    """事件类

    每一次的 :func:`Observable.fire_event` 都会相应产生一个事件。

    :params event_name: 本次事件的名称
    :params sender: 事件发送对象
    """

    event_name = None
    sender = None

    def __init__(self, event_name, sender):
        self.event_name = event_name
        self.sender = sender


class Observable(object):
    """观察者类

    可给新式类mixin，使类具有观察者特性。
    """

    observer_evt_cls = Event
    """生成事件类，会在 :func:`generate_event` 中用到，默认 :class:`Event`。
    """

    def __init__(self):
        super(Observable, self).__init__()
        self._listeners = {}

    def add_listener(self, evt_name, fn):
        """添加观察者函数。

        :params evt_name: 事件名称
        :params fn: 要注册的触发函数函数

        .. note::
           允许一个函数多次注册，多次注册意味着一次 :func:`fire_event` 多次调用。
        """
        self._listeners.setdefault(evt_name, [])
        listeners = self.__get_listeners(evt_name)
        listeners.append(fn)

    def remove_listener(self, evt_name, fn, remove_all=False):
        """删除观察者函数。

        :params evt_name: 事件名称
        :params fn: 要注册的触发函数函数
        :params remove_all: 是否删除fn在evt_name中的所有注册\n
                            如果为 `True`，则删除所有\n
                            如果为 `False`，则按注册先后顺序删除第一个\n

        .. note::
           允许一个函数多次注册，多次注册意味着一次时间多次调用。
        """
        listeners = self.__get_listeners(evt_name)
        if not self.has_listener(evt_name, fn):
            raise ObservableError(
                "function %r does not exist in the %r event",
                fn, evt_name)
        if remove_all:
            listeners[:] = [i for i in listeners if i != fn]
        else:
            listeners.remove(fn)

    def has_listener(self, evt_name, fn):
        """指定listener是否存在

        :params evt_name: 事件名称
        :params fn: 要注册的触发函数函数
        """
        listeners = self.__get_listeners(evt_name)
        return fn in listeners

    def purge_listeners(self, evt_name):
        """清除单个事件的listeners

        只清除注册到 ``evt_name`` 的事件。

        :params evt_name: 事件名称
        """
        listeners = self.__get_listeners(evt_name)
        listeners[:] = []

    def purge_all_listeners(self):
        """清除所有listeners
        """
        self._listeners = {}

    def fire_event(self, evt_name, *args, **kwargs):
        """触发事件

        :params evt_name: 事件名称
        :params args: 给事件接受者的参数
        :params kwargs: 给事件接受者的参数
        """
        listeners = self.__get_listeners(evt_name)
        evt = self.generate_event(evt_name)
        for listener in listeners:
            listener(evt, *args, **kwargs)

    def generate_event(self, evt_name):
        """生成事件方法

        可自定义此方法来产生自定义Event。如果想自定义Event类型，
        可覆盖 :attr:`observer_evt_cls`，如果需自定义生成过程，就覆
        盖此方法。

        :params evt_name: 事件名称
        """
        return self.observer_evt_cls(evt_name, self)

    def __get_listeners(self, evt_name):
        return self._listeners.get(evt_name, [])
