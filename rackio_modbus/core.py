# -*- coding: utf-8 -*-
"""rackio_modbus/core.py

This module implements the core app class and methods for Rackio Modbus.
"""

from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

from ._singleton import Singleton
from .worker import ModbusWorker

from .decorator import AppendWorker

class ModbusCore(Singleton):

    def __init__(self):

        super(ModbusCore, self).__init__()
        
        conf.SIGNED_VALUES = True

        TCPServer.allow_reuse_address = True
        self.modbus_app = get_server(TCPServer, ('localhost', 502), RequestHandler)

    def __call__(self, app):

        if not app:
            return self.modbus_app

        self.app = app
        
        self.worker = ModbusWorker(self.modbus_app)

        app._start_workers = AppendWorker(app._start_workers, self.worker)
    