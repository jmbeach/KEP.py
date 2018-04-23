"""Simulator device module"""

from lib.regular_register import RegularRegister
from lib.string_register import StringRegister
from lib.tag_type_siemens import SiemensTcpIpTagType

class SimulatorDevice(object):
    """Represents a simulator device"""

    def __init__(self, is_16bit):
        self._normal_register = RegularRegister(is_16bit)
        self._string_register = StringRegister(is_16bit)
        self._is_sixteen_bit = is_16bit
        self._tag_type_processor = {
            SiemensTcpIpTagType.BOOLEAN: self.process_boolean,
            SiemensTcpIpTagType.BOOLEAN_ARRAY: self.process_boolean_array,
            SiemensTcpIpTagType.BYTE: self.process_byte,
            SiemensTcpIpTagType.DWORD: self.process_dword,
            SiemensTcpIpTagType.DWORD_ARRAY: self.process_dword_array,
            SiemensTcpIpTagType.FLOAT: self.process_float,
            SiemensTcpIpTagType.REAL_ARRAY: self.process_real_array,
            SiemensTcpIpTagType.SHORT: self.process_short,
            SiemensTcpIpTagType.SHORT_ARRAY: self.process_short_array,
            SiemensTcpIpTagType.STRING: self.process_string,
            SiemensTcpIpTagType.WORD: self.process_word,
            SiemensTcpIpTagType.WORD_ARRAY: self.process_word_array
        }

    @property
    def normal_register(self):
        """Gets the normal register"""
        return self._normal_register

    @property
    def string_register(self):
        """Gets the string register"""
        return self._string_register

    @property
    def is_sixteen_bit(self):
        """Returns True if device is 16 bit"""
        return self._is_sixteen_bit

    def process_tag(self, tag):
        """Processes tag and detects which function to use"""
        try:
            self._tag_type_processor[tag.data_type](tag)
        except KeyError as ex:
            raise Exception('Tag type {0} not recognized for tag {1}'
                            .format(
                                tag.data_type,
                                tag.name),
                            ex)


    def process_boolean(self, tag):
        """Process Boolean type tags"""
        tag.set_address(self.normal_register.current_bit_address)
        self.normal_register.move_to_next_bit_address()

    def process_boolean_array(self, tag):
        """Process Boolean array type tags"""
        array_size = tag.get_array_size()
        tag.set_address(self.normal_register.get_array(array_size))
        if self.is_sixteen_bit:
            # each boolean address needs 1/16 byte
            self.normal_register.move_to_next_address((array_size / 16) + 1)
            return
        # each boolean address needs 1/8 byte
        self.normal_register.move_to_next_address((array_size / 8) + 1)

    def process_byte(self, tag):
        """Process byte type tags"""
        tag.set_address(self.normal_register.current_address)
        # each address needs 1 byte
        self.normal_register.move_to_next_address(1)

    def _process_32_bit_type(self, tag):
        tag.set_address(self.normal_register.current_address)
        if self.is_sixteen_bit:
            # each word address needs 4 bytes = 2 addresses
            self.normal_register.move_to_next_address(2)
            return
        # each word address needs 4 bytes = 4 addresses
        self.normal_register.move_to_next_address(4)

    def _process_16_bit_type(self, tag):
        tag.set_address(self.normal_register.current_address)
        if self.is_sixteen_bit:
            # each short address needs 2 bytes = 1 address
            self.normal_register.move_to_next_address(1)
            return
        # each short address needs 2 bytes = 2 addresses
        self.normal_register.move_to_next_address(2)

    def process_dword(self, tag):
        """Process dword type tags"""
        self._process_32_bit_type(tag)

    def process_float(self, tag):
        """Process float type tags"""
        self._process_32_bit_type(tag)

    def process_dword_array(self, tag):
        """Process dword array type tags"""
        array_size = tag.get_array_size()
        tag.set_address(self.normal_register.get_array(array_size))
        if self.is_sixteen_bit:
            # each double word address needs 4 bytes = 2 addresses
            self.normal_register.move_to_next_address(array_size * 2)
            return
        # each double word address needs 4 bytes = 4 addresses
        self.normal_register.move_to_next_address(array_size * 4)

    def process_real_array(self, tag):
        """Process real array type tags"""
        array_size = tag.get_array_size()
        tag.set_address(self.normal_register.get_array(array_size))
        if self.is_sixteen_bit:
            # each real address needs 2 bytes = 1 address
            self.normal_register.move_to_next_address(array_size)
            return
        # each real address needs 2 bytes = 2 addresses
        self.normal_register.move_to_next_address(array_size * 2)

    def process_short(self, tag):
        """Process short type tags"""
        self._process_16_bit_type(tag)

    def process_word(self, tag):
        """Process word type tags"""
        self._process_16_bit_type(tag)

    def _process_16_bit_array(self, tag):
        array_size = tag.get_array_size()
        tag.set_address(self.normal_register.get_array(array_size))
        if self.is_sixteen_bit:
            # each short address needs two bytes = 1 address
            self.normal_register.move_to_next_address(array_size)
            return
        # each short address needs two bytes = 2 addresses
        self.normal_register.move_to_next_address(array_size * 2)

    def process_short_array(self, tag):
        """Process short array type tags"""
        self._process_16_bit_array(tag)

    def process_word_array(self, tag):
        """Process short array type tags"""
        self._process_16_bit_array(tag)

    def process_string(self, tag):
        """Process string type tags"""
        tag.set_address(self.string_register.current_address)
        if self.is_sixteen_bit:
            # each string address needs 1 byte = 1/2 an address
            self.string_register.move_to_next_address(1)
            return
        # each string address needs 1 byte = 1 address
        self.string_register.move_to_next_address(1)
