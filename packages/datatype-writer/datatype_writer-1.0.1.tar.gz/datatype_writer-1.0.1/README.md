# DataType Writer

DataType Writer is a python library that allows for simple concatenation of various datatypes into a bytes object that maintains bit padding. 

## Overview

DataType Writer is a python library that creates intermediate _link_ objects for data objects, such as byte arrays, unsigned integers, or bits.

DataType Writer overwrites the functionally of _&_, _|_, _-_, and _+_. 

### & (HexDump)

Using _&_ will create a hexdump object. For example:

```python
from datatype_writer.integer import U, S
# Big Endian Concatenation
U(63, size =2) & S(-375, size = 3)
```
Would return:
```
00 3F FF FE 89
```

Similarly, if little endian is used instead, then:

```python
from datatype_writer.integer import U, S
# Little Endian Concatenation
U(63, size =2, e ='le') & S(-375, size = 3, e='le')
```

Would return:
```
3F 00 89 FE FF
```

## Installation

To install datatype writer, use the following:
```commandline
pip install datatype-writer
```