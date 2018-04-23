"""Channel module"""
from lib.device import Device

class Channel(object):
    """Represents a Kepware channel"""
    def __init__(self, channel_dict, is_sixteen_bit, ignore_list):
        self._channel_dict = channel_dict
        self._ignore_list = ignore_list
        self.set_driver_simulated()
        self._is_sixteen_bit = is_sixteen_bit
        self._devices = self.parse_devices()

    def each_device(self, work):
        """Perform work on each device.
        Work is a function whcich takes a device as a parameter"""
        for device in self._devices:
            work(device)

    def parse_devices(self):
        """Creates an array of Device objects from the channel"""
        devices = []
        for device in self._channel_dict["devices"]:
            devices.append(Device(device, self._is_sixteen_bit, self._ignore_list))
        return devices

    def set_driver_simulated(self):
        """Sets the channel driver to simulator"""
        self._channel_dict["servermain.MULTIPLE_TYPES_DEVICE_DRIVER"] = "Simulator"

    @property
    def devices(self):
        """Gets the channel devices"""
        return self._devices

    @property
    def name(self):
        """Gets the name of the device"""
        return self._channel_dict["common.ALLTYPES_NAME"]

    def as_dict(self):
        """Returns dictionary representation of the channel"""
        return self._channel_dict

    def update(self):
        """Updates the dictionary of the channel"""
        for device in self.devices:
            device.update()
        for i in range(len(self._channel_dict["devices"])):
            device_dict = self._channel_dict["devices"][i]
            for device in self._devices:
                if device.name == device_dict["common.ALLTYPES_NAME"]:
                    self._channel_dict["devices"][i] = device.as_dict()
