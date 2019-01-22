"""Simulator device module"""

from keppy.regular_register import RegularRegister
from keppy.string_register import StringRegister
from keppy.tag_data_type import TagDataType

class SimulatorDevice(object):
    """Represents a simulator device"""

    def __init__(self, is_16bit, normal_register_initial_address="K0000", string_register_initial_address="S000"):
        self._normal_register = RegularRegister(is_16bit, normal_register_initial_address)
        self._string_register = StringRegister(is_16bit, string_register_initial_address)
        self._is_sixteen_bit = is_16bit
        self._tag_type_processor = {
            TagDataType.BOOLEAN: self.process_boolean,
            TagDataType.BOOLEAN_ARRAY: self.process_boolean_array,
            TagDataType.BYTE: self.process_byte,
            TagDataType.DWORD: self.process_dword,
            TagDataType.LONG: self.process_dword,
            TagDataType.DWORD_ARRAY: self.process_dword_array,
            TagDataType.FLOAT: self.process_float,
            TagDataType.REAL_ARRAY: self.process_real_array,
            TagDataType.SHORT: self.process_short,
            TagDataType.SHORT_ARRAY: self.process_short_array,
            TagDataType.STRING: self.process_string,
            TagDataType.WORD: self.process_word,
            TagDataType.WORD_ARRAY: self.process_word_array,
            TagDataType.LLONG: self._process_64_bit_type,
            TagDataType.QWORD: self._process_64_bit_type,
            TagDataType.DOUBLE: self._process_64_bit_type
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
            if not self._is_function(tag):
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

    def _process_64_bit_type(self, tag):
        tag.set_address(self.normal_register.current_address)
        if self.is_sixteen_bit:
            # each qword address needs 8 bytes = 4 addresses
            self.normal_register.move_to_next_address(4)
            return
        # each qword address needs 8 bytes = 8 addresses
        self.normal_register.move_to_next_address(8)

    def _process_32_bit_type(self, tag):
        tag.set_address(self.normal_register.current_address)
        if self.is_sixteen_bit:
            # each dword address needs 4 bytes = 2 addresses
            self.normal_register.move_to_next_address(2)
            return
        # each dword address needs 4 bytes = 4 addresses
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

    def _is_function(self, tag):
        function_names = ['USER', 'RAMP', 'SINE', 'RANDOM']
        for function_name in function_names:
            if function_name in tag.get_address():
                return True
        return False
