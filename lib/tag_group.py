"""Kepware tag group module"""
from lib.tag import Tag
class TagGroup(object):
    """Represents a Kepware tag group"""
    def __init__(self, tag_group_dict):
        self._tag_group_dict = tag_group_dict
        self._tags = self.parse_tags()
        self._is_ignored = False

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

    def as_dict(self):
        """Returns dictionary representation of the tag group"""
        return self._tag_group_dict

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
