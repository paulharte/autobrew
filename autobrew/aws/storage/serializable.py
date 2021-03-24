import datetime
import json


class Serializable:
    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(
            self, default=lambda o: convert_to_json(o), sort_keys=True, indent=4
        )

    @classmethod
    def from_json(cls, json_string):
        attributes = json.loads(json_string)
        if not isinstance(attributes, dict):
            raise ValueError
        return cls.from_dict(attributes)

    @classmethod
    def from_dict(cls, attributes):
        if attributes is None:
            return
        obj = cls()
        obj.__dict__ = attributes
        return obj


def convert_to_json(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    else:
        return obj.__dict__
