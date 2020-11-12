# rackio_modbus/_server.py

from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server

from Rackio import TagEngine


class FloatTagMap:

    def __init__(self, tag, upper, lower):

        self.tag = tag
        self.upper = upper
        self.lower = lower

    def register(self, value):

        upper = self.upper
        lower = self.lower

        return int(((value - lower) / (upper - lower)) * 65535)

    def value(self, register):

        upper = self.upper
        lower = self.lower

        return (register / 65535) * (upper - lower) + lower


class IntTagMap:

    def __init__(self, tag, upper, lower):

        self.tag = tag
        self.upper = upper
        self.lower = lower

    def register(self, value):

        upper = self.upper
        lower = self.lower

        return int(((value - lower) / (upper - lower)) * 65535)

    def value(self, register):

        upper = self.upper
        lower = self.lower

        return int((register / 65535) * (upper - lower) + lower)


class BooleanTagMap:

    def __init__(self, tag):

        self.tag = tag

    def coil(self, value):

        if value:
            return 1
        return 0

    def value(self, coil):

        if coil == 1:
            return True
        return False


class ModbusServer():

    def __init__(self):

        conf.SIGNED_VALUES = True
        TCPServer.allow_reuse_address = True

        self.app = get_server(TCPServer, ('localhost', 502), RequestHandler)

        self.mappings = list()
        self.input_registers = list()
        self.holding_registers = list()
        self.coils = list()
        self.discrete = list()

    def get_driver(self):

        return self.app

    def define_mapping(self, tag, direction, upper, lower):

        engine = TagEngine()

        _type = engine.get_type(tag)

        if _type == "float":
            mapping = FloatTagMap(tag, upper, lower)

            if direction == "write":
                self.holding_registers.append(mapping)
            else:
                self.input_registers.append(mapping)

        elif _type == "int":
            mapping = IntTagMap(tag, upper, lower)

            if direction == "write":
                self.holding_registers.append(mapping)
            else:
                self.input_registers.append(mapping)
        elif _type == ["bool"]:
            mapping = BooleanTagMap(tag)

            if direction == "write":
                self.discrete.append(mapping)
            else:
                self.coils.append(mapping)

    def write_register(self, slave_id, function_code, address, value):

        engine = TagEngine()

        mapping = self.holding_registers[address]
        tag = mapping.tag

        value = mapping.value(value)
        engine.write_tag(tag, value)

    def read_register(self, slave_id, function_code, address):
        
        engine = TagEngine()
        
        if function_code == 3:
            mapping = self.holding_registers[address]
        elif function_code == 4:
            mapping = self.input_registers[address]

        tag = mapping.tag

        value = engine.read_tag(tag)

        return mapping.register(value)

    def write_coil(self, slave_id, function_code, address, value):

        engine = TagEngine()

        mapping = self.coils[address]
        tag = mapping.tag

        value = mapping.value(value)
        engine.write_tag(tag, value)

    def read_input(self, slave_id, function_code, address):
        
        engine = TagEngine()
        
        if function_code == 1:
            mapping = self.coils[address]
        elif function_code == 2:
            mapping = self.discrete[address]

        tag = mapping.tag

        value = engine.read_tag(tag)

        return mapping.coil(value)
    