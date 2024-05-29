from datatype_writer.integer import Integer
from datatype_writer.string import String
from datatype_writer.bit import Bit
from datatype_writer.byte_array import ByteArray

import yaml
import os
import random
import re


def get_max(size, signed):
    if signed:
        return int((2 ** (8 * size)) / 2 - 1)
    else:
        return int((2 ** (8 * size)) - 1)


def get_min(size, signed):
    if signed:
        return -1 * int((2 ** (8 * size)) / 2)
    else:
        return 0


def get_random_byte_array(size):
    ba = b''
    for _ in range(size):
        ba += int(random.randint(0, 255)).to_bytes(length=1, byteorder='big')
    return ba


def get_random_bits(size):
    bits = ""
    for _ in range(size):
        bits += '10'[random.randint(0, 1)]
    return bits


def get_random_string(count):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    rtn_str = ""
    for _ in range(count):
        rtn_str += letters[random.randint(0, len(letters) - 1)]


def get_random_int(contraint, size, signed):
    min = None
    max = None
    must_be = None
    any_of = None
    none_of = None
    if contraint is not None:
        if type(contraint) == int:
            must_be = contraint
        elif 'eq' in contraint.keys():
            must_be = contraint['eq']
        if 'max' in contraint.keys():
            max = contraint['max']
        if 'min' in contraint.keys():
            min = contraint['min']
        if 'any-of' in contraint.keys():
            any_of = contraint['any-of']
        if 'none-of' in contraint.keys():
            none_of = contraint['none_of']
    if min is not None and max is not None:
        return random.randint(min, max)
    if min is not None:
        return random.randint(min, get_max(size, signed))
    if max is not None:
        return random.randint(get_min(size, signed), max)
    if must_be is not None:
        return must_be
    if any_of is not None:
        return any_of[random.randint(0, len(any_of) - 1)]
    if none_of is not None:
        while True:
            candidate = random.randint(get_min(size, signed), get_max(size, signed))
            if candidate not in none_of:
                return candidate

    return random.randint(get_min(size, signed), get_max(size, signed))


def read_spec(yaml_path):
    if not os.path.exists(yaml_path):
        raise Exception(f"{yaml_path} not found.")

    with open(yaml_path) as file_in:
        return yaml.safe_load(file_in)


def get_size(t):
    i = re.search(r"\d+", t)
    if i is not None:
        return i.group(0)
    else:
        # TODO: find the default
        return 1


def get_endian(t):
    i = re.search(r"le", t)
    if i is not None:
        return "le"
    i = re.search(r"be", t)
    if i is not None:
        return "be"
    return None


class Specification:
    def __init__(self, yaml_path):
        self.spec = read_spec(yaml_path)
        self.enums = None
        self.types = None
        self.default_endian = None
        self.fields = None
        self.process_spec()

    def get_spec(self):
        return self.spec

    def get_repr(self):
        # return the repr of the individual components
        pass

    def get_spec_fields(self):
        return self.fields

    def add_field(self, field):
        self.fields.append(field)

    def field_count(self):
        return len(self.fields)

    def process_spec(self):
        self.default_endian = self.spec['meta']['endian']
        self.enums = self.spec['enums']
        self.types = self.spec['types']
        self.process_seq(self.spec['seq'])

    def get_field_value(self, key):
        for f in self.fields:
            if f.id == key:
                if f.content.data is None:
                    # call self generate data
                    return f.content.data
                else:
                    return f.content.data

    def get_field(self, key):
        for f in self.fields:
            if f.id == key:
                return f

    def process_seq(self, seq):
        for field in seq:
            if 'contains' in field.keys():
                # TODO Add processing for contains constant types
                pass

            elif 'type' in field.keys():
                if type(field['type']) == dict:
                    # If the type is a switch case, choose a value for the reference field then
                    # process the appropriate sequence.
                    field_id = field['type']['switch-on']
                    values = field['type']['cases'].keys()
                    choice = random.randint(0, len(values) - 1)
                    case_value = values[choice]
                    if choice == (len(values) - 1):
                        ref_field = self.get_field(field_id)
                        ref_field.set_constraint({'none-of': [v for v in values[:-1]]})
                        ref_field.assign_value()
                    else:
                        ref_field = self.get_field(field_id)
                        ref_field.content.set_data(case_value)

                    seq_type = field['type']['cases'][case_value]
                    self.process_seq(self.types[seq_type])

                elif field['type'] in self.types.keys(): # The type is a named sequence
                    self.process_seq(self.types[seq['type']])
                else: # The type is an atomic type of int, bit, or str
                    self.process_atomic_field(field)
            else:
                self.process_byte_array(field)

    def process_atomic_field(self, field):
        temp_field = Field()
        temp_field.set_id(field['id'] if 'id' in field.keys() else "")
        t = field['type']
        temp_field.set_type(t)
        if t.find('str') != 0:
            temp_field.set_content(self.process_atomic_string(field))
        elif t[0] == 'u':
            temp_field.set_content(self.process_atomic_signed_int(field, False))
        elif t[0] == 's':
            temp_field.set_content(self.process_atomic_signed_int(field, True))
        elif t[0] == 'b':
            temp_field.set_content(self.process_atomic_bit(field))

        if 'valid' in field.keys():
            temp_field.set_constraint(field['valid'])
        temp_field.set_position(self.field_count())
        temp_field.assign_value()
        self.add_field(temp_field)

    def process_atomic_string(self, field):
        if type(field['size']) == int:
            size = field['size']
        else:
            size = self.get_field_value(key=field['size'])
        if 'encoding' in field.keys():
            encoding = field['encoding'].lower()
        else:
            encoding = 'utf-8'
        return String(None, self.default_endian, size, encoding)

    def process_atomic_signed_int(self, field, signed):
        size = get_size(field['type'])
        endian = get_endian(field['type']) if get_endian(field['type']) is not None else self.default_endian
        return Integer(None, size, endian, signed=signed)

    def process_atomic_bit(self, field):
        size = get_size(field['type'])
        return Bit(None, size)

    def process_byte_array(self, field):
        temp_field = Field()
        temp_field.set_id(field['id'] if 'id' in field.keys() else "")
        temp_field.set_type("BYTES")

        if type(field['size']) == int:
            size = field['size']
        else:
            size = self.get_field_value(key=field['size'])

        content = ByteArray(None, endianess=self.default_endian, size=size)
        temp_field.set_content(content)
        temp_field.set_position(self.field_count())
        self.add_field(temp_field)

    def write_spec_to_file(self, file):
        receipt = []
        bit_buffer = None
        with open(file, "wb") as file_out:
            for field in self.fields:
                if type(field) == Bit:
                    if bit_buffer is None:
                        bit_buffer = field
                    else:
                        bit_buffer = bit_buffer + field
                else:
                    if bit_buffer is not None:
                        file_out.write(bit_buffer.get_bytes())
                        receipt.append(bit_buffer.__repr__())
                        bit_buffer = None
                    file_out.write(field.get_bytes())
                    receipt.append(field.__repr__())
        return receipt

    def get_hex_dump(self):
        dumps = []
        bit_buffer = None
        for field in self.fields:
            if type(field) == Bit:
                if bit_buffer is None:
                    bit_buffer = field
                else:
                    bit_buffer = bit_buffer + field
            else:
                if bit_buffer is not None:
                    dumps.append(bit_buffer.get_hex_dump())
                    bit_buffer = None
                dumps.append(field.get_hex_dump())
        return " ".join(dumps)

class Field:
    def __init__(self):
        self.content = None
        self.constraint = None
        self.position = None
        self.id = None
        self.type_literal = None
        self.enum = None
        self.exclusions = None

    def set_id(self, value):
        self.id = value

    def set_type(self, value):
        self.type_literal = value

    def set_content(self, content):
        self.content = content

    def set_constraint(self, constraint):
        self.constraint = constraint

    def set_position(self, pos):
        self.position = pos

    def update_content_value(self, value):
        self.content.data = value

    def assign_value(self):
        size = self.content.size
        if type(self.content) == String:
            self.content.set_data(get_random_string(size))
        elif type(self.content) == Integer:
            signed = self.content.signed
            self.content.set_data(get_random_int(self.contraint, size, signed))
        elif type(self.content) == ByteArray:
            self.content.set_data(get_random_byte_array(size))
        elif type(self.content) == Bit:
            self.content.set_data(get_random_bits(size))
