"""Kepware project module"""
import json
from collections import OrderedDict
from lib.channel import Channel

class Project(object):
    """Represents a Kepware project"""
    def __init__(self, kepware_dict, is_sixteen_bit, ignore_list):
        self._ignore_list = ignore_list
        self._kepware_dict = kepware_dict
        self._project_dict = kepware_dict["Project"]
        self._is_sixteen_bit = is_sixteen_bit
        self._channels = self.parse_channels()

    @property
    def channels(self):
        """Gets the channels of the project"""
        return self._channels

    def parse_channels(self):
        """Creates an array of Channel objects from the project"""
        channels = []
        for channel in self._project_dict["channels"]:
            channels.append(Channel(channel, self._is_sixteen_bit, self._ignore_list))
        return channels

    def as_json(self):
        """Returns the stringified JSON representation of the Kepware
        project"""
        return json.dumps(OrderedDict(self._kepware_dict))

    def update(self):
        """Updates the dictionary of the project"""
        for channel in self.channels:
            channel.update()
        for i in range(len(self._project_dict["channels"])):
            channel_dict = self._project_dict["channels"][i]
            for channel in self.channels:
                if channel.name == channel_dict["common.ALLTYPES_NAME"]:
                    self._project_dict["channels"][i] = channel.as_dict()
