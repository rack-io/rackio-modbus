# rackio_modbus/_server.py

from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server


class TagMap:

    def __init__(self, tag, direction, upper, lower):

        self.tag = tag
        self.direction = direction
        self.upper = upper
        self.lower = lower

    def register(self, value):

        upper = self.upper
        lower = self.lower

        return ((value - lower) / (upper - lower)) * 65535

    def value(self, register):

        upper = self.upper
        lower = self.lower

        return (register / 65535) * (upper - lower) + lower


class ModbusServer():

    def __init__(self):

        conf.SIGNED_VALUES = True
        TCPServer.allow_reuse_address = True

        self.app = get_server(TCPServer, ('localhost', 502), RequestHandler)

        self.mappings = list()

    def define_mapping(self, tag, direction, upper, lower):

        mapping = TagMap(tag, direction, upper, lower)

        self.mappings.append(mapping)

    def set_mappings(self):

        pass
    