"""Kepware device module"""
from lib.tag_group import TagGroup

class Device(object):
    """Represents a Kepware device"""
    def __init__(self, device_dict, is_sixteen_bit, ignore_list):
        self._ignore_list = ignore_list
        self._device_dict = device_dict
        self._tag_groups = self.parse_tag_groups()
        self._is_sixteen_bit = is_sixteen_bit
        self.set_driver_simulated()

    def set_driver_simulated(self):
        """Sets the device driver type to simulated"""
        self._device_dict["servermain.MULTIPLE_TYPES_DEVICE_DRIVER"] = "Simulator"
        if self._is_sixteen_bit:
            self._device_dict["servermain.DEVICE_MODEL"] = 0
        else:
            self._device_dict["servermain.DEVICE_MODEL"] = 1
        self._device_dict["servermain.DEVICE_ID_OCTAL"] = 1

    def parse_tag_groups(self):
        """Gets an array of TagGroup objects in the Kepware device"""
        tag_groups = []
        if 'tag_groups' not in self._device_dict:
            return tag_groups
        to_remove = []
        for tag_group in self._device_dict['tag_groups']:
            if tag_group['common.ALLTYPES_NAME'] in self._ignore_list:
                to_remove.append(tag_group)
                continue
            tag_groups.append(TagGroup(tag_group))
        for removable in to_remove:
            self._device_dict['tag_groups'].remove(removable)

        return tag_groups

    @property
    def tag_groups(self):
        """Gets the tag groups of the device"""
        return self._tag_groups

    @property
    def is_sixteen_bit(self):
        """Returns true if is sixteen bit device"""
        return self._is_sixteen_bit

    @property
    def name(self):
        """Gets the name of the device"""
        return self._device_dict["common.ALLTYPES_NAME"]

    def as_dict(self):
        """Returns dictionary representation of the device"""
        return self._device_dict

    def update(self):
        """Updates the dictionary of the device"""
        if "tag_groups" not in self._device_dict:
            return
        for group in self.tag_groups:
            group.update()
        for i in range(len(self._device_dict["tag_groups"])):
            tag_group_dict = self._device_dict["tag_groups"][i]
            for group in self.tag_groups:
                if group.name == tag_group_dict["common.ALLTYPES_NAME"]:
                    self._device_dict["tag_groups"][i] = group.as_dict()
