from datatype_writer.link import Link, HexLink, ByteLink


def hex_dump(byte_array, endianess='be'):
    str_array = [hex(b)[2:].zfill(2).upper() for b in byte_array]
    if endianess == 'le':
        str_array = str_array[::-1]
    return " ".join(str_array)


class Format:
    def __init__(self, data, endianess='be'):
        self.data = data
        self.endianess = endianess

    def get_bytes(self):
        pass

    def get_hex_dump(self):
        pass

    def __and__(self, other):
        return HexLink(self.get_hex_dump() + " " + other.get_hex_dump())

    def __or__(self, other):
        return ByteLink(self.get_bytes() + other.get_bytes())

    def __add__(self, other):
        return Link(self.get_hex_dump() + " " + other.get_hex_dump(), self.get_bytes() + self.get_bytes())

    def __str__(self):
        return self.get_hex_dump()

    def __repr__(self):
        return f'Format({self.data},{self.endianess})'

    def set_data(self, value):
        self.data = value

