from datatype_writer.format import Format


class Integer(Format):
    def __init__(self, data, endianess='be', size=1, signed=False):
        Format.__init__(self, data,  "big" if endianess == 'be' else 'little')
        self.size = size
        self.signed = signed

    def get_bytes(self):
        return int(self.data).to_bytes(length=self.size, byteorder=self.endianess, signed=self.signed)

    def get_hex_dump(self):
        byte_array = self.get_bytes()
        hex_dump = [hex(b)[2:].zfill(2) for b in byte_array]
        return " ".join(hex_dump).upper()

    def __repr__(self):
        return f"Integer({self.data},{self.endianess},{self.size},{self.signed})"

class S(Integer):
    def __init__(self, data, e='be', size=1):
        endian = "big" if e == 'be' else 'little'
        Integer.__init__(self, data, endian, size, True)


class U(Integer):
    def __init__(self, data, e='be', size=1):
        endian = "big" if e == 'be' else 'little'
        Integer.__init__(self, data, endian, size, False)
