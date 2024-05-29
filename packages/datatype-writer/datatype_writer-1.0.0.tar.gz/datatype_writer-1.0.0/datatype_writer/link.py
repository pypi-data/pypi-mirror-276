class Link:
    def __init__(self, hex_data, bytes_data):
        self.hex_data = hex_data
        self.bytes_data = bytes_data

    def get_bytes(self):
        return self.bytes_data

    def get_hex_dump(self):
        return self.hex_data

    def get_writable(self, idx=0):
        if idx == 0:
            return self.get_bytes()
        if idx == 1:
            return self.get_hex_dump()

    def __add__(self, other):
        return Link(self.hex_data + " " + other.get_hex_dump(), self.bytes_data + other.get_bytes())

    def __str__(self):
        return self.hex_data

    def __repr__(self):
        return self.hex_data, str(self.bytes_data)


class HexLink:
    def __init__(self, hex_data):
        self.hex_data = hex_data

    def get_hex_dump(self):
        return self.hex_data

    def get_writable(self):
        return self.hex_data

    def __and__(self, other):
        return HexLink(self.hex_data + " " + other.get_hex_dump())

    def __str__(self):
        return self.hex_data

    def __repr__(self):
        return self.hex_data


class ByteLink:
    def __init__(self, bytes_data):
        self.bytes_data = bytes_data

    def get_bytes(self):
        return self.bytes_data

    def get_writable(self):
        return self.get_bytes()

    def __or__(self, other):
        return HexLink(self.bytes_data + other.get_bytes())

    def __str__(self):
        return str(self.bytes_data)

    def __repr__(self):
        return str(self.bytes_data)
