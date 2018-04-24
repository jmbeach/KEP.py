"""Tag type group module"""

from enum import Enum

class SiemensTcpIpTagType(Enum):
    """Enum for siemens TCP / IP data types"""
    STRING = 0
    BOOLEAN = 1
    BYTE = 3
    SHORT = 4
    WORD = 5
    DWORD = 7
    FLOAT = 8
    BOOLEAN_ARRAY = 21
    SHORT_ARRAY = 24
    WORD_ARRAY = 25
    DWORD_ARRAY = 27
    REAL_ARRAY = 28
