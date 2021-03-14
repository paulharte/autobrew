import json


class Serializable:
    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

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
