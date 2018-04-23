"""Kepware tag module"""

import re
from lib.tag_type_siemens import SiemensTcpIpTagType

class Tag(object):
    """Represents a kepware tag"""
    def __init__(self, tag_dict):
        self._tag_dict = tag_dict
        self.address = property(self.get_address, self.set_address)

    @property
    def name(self):
        """The name of the tag"""
        return self._tag_dict["common.ALLTYPES_NAME"]

    @property
    def data_type(self):
        """Gets tag data type"""
        return SiemensTcpIpTagType(int(self._tag_dict["servermain.TAG_DATA_TYPE"]))

    def get_address(self):
        """Gets tag address"""
        return self._tag_dict["servermain.TAG_ADDRESS"]

    def set_address(self, value):
        """Sets tag address"""
        self._tag_dict["servermain.TAG_ADDRESS"] = value

    def name_replace(self, to_replace, replacement):
        """Replaces part of tag name with new value"""
        self.name = self.name.replace(to_replace, replacement)

    def as_dict(self):
        """Returns dictionary representation of the tag"""
        return self._tag_dict

    def get_array_size(self):
        """Attempts to parse array size out of the address"""
        match = re.search(r"(?<=\[)\d+(?=\])", self.get_address())
        return int(match.group(0))

    def get_string_length(self):
        """Attempts to parse array size out of the address"""
        try:
            return self.get_array_size()
        except:
            match = re.search(r"(?<=\.)\d+", self.get_address())
            try:
                return int(match.group(0))
            except Exception as ex:
                raise Exception('Could not get string size of {0} address {1}'
                                .format(
                                    self.name,
                                    self.get_address()),
                                ex)
