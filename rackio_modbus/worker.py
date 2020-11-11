# -*- coding: utf-8 -*-
"""rackio_socket/core.py

This module implements the core app class and methods for Rackio Socket.
"""

from threading import Thread


class ModbusWorker(Thread):

    def __init__(self, app, *args, **kwargs):

        super(ModbusWorker, self).__init__(*args, **kwargs)

        self.app = app

    def run(self):

        try:
            self.app.serve_forever()
        finally:
            self.app.shutdown()
            self.app.server_close()
