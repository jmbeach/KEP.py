"""Kepware tag group module"""
import json
from collections import OrderedDict

from keppy.tag import Tag
class TagGroup(object):
    """Represents a Kepware tag group"""
    def __init__(self, tag_group_dict):
        self._tag_group_dict = tag_group_dict
        self._tags = self.parse_tags()
        self._is_ignored = False
        self._sub_groups = []
        # process sub groups
        if "tag_groups" in self._tag_group_dict:
            for sub_group in self._tag_group_dict["tag_groups"]:
                self._sub_groups.append(TagGroup(sub_group))

    def parse_tags(self):
        """Parses tags in tag group"""
        tags = []
        try:
            for tag in self._tag_group_dict["tags"]:
                tags.append(Tag(tag))
        except:
            return tags
        return tags

    @property
    def tags(self):
        """Gets the tags of the tag group"""
        return self._tags

    @property
    def name(self):
        """Gets the name of the tag group"""
        if self._is_ignored:
            return ''
        return self._tag_group_dict["common.ALLTYPES_NAME"]
    
    @property
    def sub_groups(self):
        return self._sub_groups

    def as_dict(self):
        """Returns dictionary representation of the tag group"""
        return self._tag_group_dict

    def as_json(self):
        """Returns the stringified JSON representation of the Kepware
        tag group"""
        return json.dumps(OrderedDict(self._tag_group_dict))

    def set_name(self, name):
        self._tag_group_dict["common.ALLTYPES_NAME"] = name

    def update(self):
        """Updates the dictionary of the tag group"""
        if self._is_ignored or "tags" not in self._tag_group_dict:
            return
        for i in range(len(self._tag_group_dict["tags"])):
            tag_dict = self._tag_group_dict["tags"][i]
            for tag in self._tags:
                if tag.name == tag_dict["common.ALLTYPES_NAME"]:
                    self._tag_group_dict["tags"][i] = tag.as_dict()
                    break

        for i in range(len(self._sub_groups)):
            sub_group = self._sub_groups[i]
            sub_group.update()
            self._tag_group_dict["tag_groups"][i] = sub_group.as_dict()
