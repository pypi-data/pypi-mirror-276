from datatype_writer.format import Format


class ByteArray(Format):
    def __init__(self, data, endianess='be', size=1):
        Format.__init__(self, data, endianess)
        self.size = size

    def get_bytes(self):
        if self.endianess == "le":
            return self.data[::-1]
        else:
            return self.data

    def get_hex_dump(self):
        byte_array = self.get_bytes()
        hex_dump = [hex(b)[2:].zfill(2) for b in byte_array]
        return " ".join(hex_dump).upper()

    def __repr__(self):
        return f"ByteArray({self.data},{self.endianess},{self.size})"