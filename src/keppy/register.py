"""Base register module"""
def pad_zeroes(addr, n_zeroes):
    """Padds the address with zeroes"""
    if len(addr) < n_zeroes:
        return pad_zeroes("0" + addr, n_zeroes)
    return addr

def int_addr(addr):
    """Gets the integer representation of an address"""
    return int(addr[1:])

def next_addr(addr, i):
    """Gets address after the current + i"""
    str_addr = pad_zeroes(str(int_addr(addr) + i), len(addr[1:]))
    return addr[0] + str_addr

class Register(object):
    """Represents the register of a simulator"""

    def __init__(self, is_16bit, initial_address):
        self._current_address = initial_address
        self._register_map = {}
        self._size_of_current_register_address = 4
        self.mark_address(initial_address, self._size_of_current_register_address)
        self._current_bit_address = ""
        self._is_16bit = is_16bit

    @property
    def current_address(self):
        """Gets the current constant address of the register."""
        return self._current_address

    @property
    def is_16bit(self):
        """Gets whether the device is 16-bit
        (or else 8-bit)"""
        return self._is_16bit

    @property
    def current_bit_address(self):
        """Gets the current bit address"""
        return self._current_bit_address

    def get_register_letter(self):
        """Gets the letter representing the register (R, K, or S)
        """
        return self._current_address[0]

    def mark_address(self, addr, size):
        """Marks address as being used in simulator"""
        i = 0
        while i < size:
            self._register_map[addr] = True
            i += 1

    def is_address_in_use(self, addr):
        """Returns value which determines if register address in use"""
        return self._register_map.get(addr)

    def next_address_avoid_collision(self, start_addr):
        """Finds the next address recursively which does not collide with any other address"""
        for i in range(1, self._size_of_current_register_address):
            str_addr = next_addr(start_addr, i)
            if self.is_address_in_use(str_addr):
                return self.next_address_avoid_collision(
                    next_addr(start_addr, self._size_of_current_register_address + 1))
        return next_addr(start_addr, self._size_of_current_register_address)

    def next_address(self):
        """Returns the next address after the current"""
        return self.next_address_avoid_collision(self._current_address)

    def move_to_next_address(self, size_of_current):
        """Moves the register's current address to the next available.
        size_of_current specifies how many bytes/words to skip"""
        self._size_of_current_register_address = size_of_current
        self._current_address = self.next_address()
        self.mark_address(self._current_address, size_of_current)

    def move_to_next_bit_address(self):
        """Moves to next available bit address position"""
        self._current_bit_address = self.next_bit_address()

    def get_array(self, array_size):
        """Gets an array address"""
        return "{0}[{1}]".format(self._current_address, array_size)

    def next_bit_address(self):
        """Gets the next boolean address"""
        if self._current_bit_address == "":
            if self._is_16bit:
                return "{0}.{1}".format(
                    self.next_address(),
                    "00")
            return "{0}.{1}".format(
                self.next_address(),
                "0")
        if self._is_16bit:
            bool_half = int(self._current_bit_address.split(".")[1])
            if bool_half < 4:
                register_half = self._current_bit_address.split(".")[0]
                return "{0}.{1}".format(
                    register_half,
                    pad_zeroes(str(bool_half + 1), 2))
            self.move_to_next_address(self._size_of_current_register_address)
            return "{0}.{1}".format(
                self.next_address(),
                "00")
        bool_half = int(self._current_bit_address.split(".")[1])
        if bool_half < 3:
            register_half = self._current_bit_address.split(".")[0]
            return "{0}.{1}".format(
                register_half,
                bool_half + 1)
        self.move_to_next_address(self._size_of_current_register_address)
        return "{0}.{1}".format(
            self.next_address(),
            "0")
