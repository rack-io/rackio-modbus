# -*- coding: utf-8 -*-
"""rackio_modbus/core.py

This module implements the core app class and methods for Rackio Modbus.
"""

import socket
from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.client import tcp
from umodbus.utils import log_to_stream

from ._singleton import Singleton
from .worker import ModbusWorker

from .decorator import AppendWorker

class ModbusCore(Singleton):

    def __init__(self):

        super(ModbusCore, self).__init__()

        self.modbus_driver = None

    def define_server(self):

        conf.SIGNED_VALUES = True

        TCPServer.allow_reuse_address = True
        return get_server(TCPServer, ('localhost', 502), RequestHandler)

    def define_client(self, *args, **kwargs):

        remote = kwargs["remote"]

        conf.SIGNED_VALUES = True

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((remote, 502))

        return {"socket": sock, "tcp": tcp}

    def __call__(self, app=None, mode="server", *args, **kwargs):

        if not app:
            return self.modbus_driver

        if mode == "server":
            self.modbus_driver = self.define_server()
        else:
            self.modbus_driver = self.define_client()
        
        self.worker = ModbusWorker(self.modbus_driver, mode)

        app._start_workers = AppendWorker(app._start_workers, self.worker)

        return self.modbus_driver
    