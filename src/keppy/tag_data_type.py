"""Tag type group module"""

from enum import Enum

class TagDataType(Enum):
    """Enum for tag data types"""
    STRING = 0
    BOOLEAN = 1
    BYTE = 3
    SHORT = 4
    WORD = 5
    LONG = 6
    DWORD = 7
    FLOAT = 8
    DOUBLE = 9
    LLONG = 13
    QWORD = 14
    BOOLEAN_ARRAY = 21
    SHORT_ARRAY = 24
    WORD_ARRAY = 25
    DWORD_ARRAY = 27
    REAL_ARRAY = 28
