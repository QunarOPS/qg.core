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


import sys

from oslo_config import cfg

from qg.core import exception
from qg.core.singleton import Singleton
from qg.core.observer import Observable


class NotInitializedError(exception.QException):
    message = 'Not initialized: %(what)s'


class FunctionNotFoundError(exception.QException):
    message = "no such function %(fn_name)s to invoke."


class QApplicationError(exception.QException):
    message = "QApplication error: %(msg)s"


class QExtensionManager(Observable):

    def __init__(self):
        super(QExtensionManager, self).__init__()
        self.steps = ["init_app", "configure", "run", "shutdown"]

    def _try_add_listener(self, ext, evt_name):
        fn = getattr(ext, evt_name, None)
        if fn is not None:
            self.add_listener(evt_name, fn)

    def append(self, ext):
        assert(isinstance(ext, QExtension))
        for step in self.steps:
            self._try_add_listener(ext, "pre_%s" % step)
            self._try_add_listener(ext, "post_%s" % step)


class QExtension(object):

    @property
    def name(self):
        return self.__class__.__name__

    def __init__(self):
        super(QExtension, self).__init__()
        if self.name is None:
            raise NotInitializedError(
                what="%s.name" % self.__class__.__name__)


class QApplication(Singleton):

    version = None

    def init_singleton(self):
        if self.name is None:
            raise NotInitializedError(
                what="%s.name" % self.__class__.__name__)
        if self.version is None:
            raise NotInitializedError(
                what="%s.version" % self.__class__.__name__)
        self.create()
        self._step_invoke("init_app")

    def create(self):
        self._ext_mgr = QExtensionManager()

    def configure(self, argv=None):
        is_argv_specified = False
        if isinstance(argv, (list, tuple)):
            is_argv_specified = True
            argv = [sys.argv[0]] + list(argv)
        if not is_argv_specified:
            argv = sys.argv
        cfg.CONF(argv[1:], project=self.name, version=self.version,
                 default_config_files=None)

    def _step_invoke(self, fn_name, do_pre=True, do_fn=True, do_post=True):
        fn = None
        rlt = None
        try:
            fn = getattr(self, fn_name)
        except AttributeError:
            raise FunctionNotFoundError(fn_name=fn_name)
        if not do_fn and do_post:
            raise QApplicationError(
                msg="Function %s must invoke if use do_post." % fn_name)
        if do_pre:
            self._ext_mgr.fire_event("pre_%s" % fn_name, self)
        if do_fn:
            rlt = fn()
        if do_post:
            self._ext_mgr.fire_event("post_%s" % fn_name, self, rlt)

    def main(self):
        self._step_invoke("configure")
        self._step_invoke("run")
        self._step_invoke("shutdown")

    def make_entry_point(self):
        def wrap():
            self.main()
        return wrap

    def register_extension(self, ext):
        self._ext_mgr.append(ext)

    def init_app(self):
        pass

    def shutdown(self):
        pass

    def run(self):
        raise NotImplementedError(
            "app.run() is not implemented yet")

    @property
    def name(self):
        return self.__class__.__name__
