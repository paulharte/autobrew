import json


class Serializable:
    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.toDict(), sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, json_string):
        attributes = json.loads(json_string)
        if not isinstance(attributes, dict):
            raise ValueError
        return cls.from_dict(attributes)

    @classmethod
    def from_dict(cls, attributes):
        obj = cls()
        obj.__dict__ = attributes
        return obj


class Brew(Serializable):
    id: str
    name: str
    active = False

    def __init__(self):
        pass

    # TODO: add validation here
