from datatype_writer.format import Format
from math import ceil


class Bit(Format):
    def __init__(self, val, size, endianess='be'):
        Format.__init__(self, None, "big" if endianess == 'be' else 'little')
        self.bits = None
        self.size = size
        if val is not None:
            self.set_data(val)
        else:
            self.data = None

    def get_bytes(self):
        return int(self.bits, 2).to_bytes(length=max(ceil(self.size / 8), 1), byteorder=self.endianess)

    def get_hex_dump(self):
        byte_array = self.get_bytes()
        hex_dump = [hex(b)[2:].zfill(2) for b in byte_array]
        return " ".join(hex_dump).upper()

    def __sub__(self, other):
        return Bit(self.bits + other.bits, self.size + other.size)

    def set_data(self, value):
        if type(value) == int:
            self.bits = bin(value)[2:].zfill(self.size)
        elif type(value) == str:
            self.bits = value

    def __repr__(self):
        return f"Bit({self.bits}{self.size}{self.endianess})"