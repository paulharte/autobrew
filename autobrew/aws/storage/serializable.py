import datetime
import json
import logging
from decimal import Decimal
from enum import Enum
from json import JSONDecodeError

DECIMAL_PRECISION = 4


class Serializable:
    def to_dict(self):
        attributes = self.__dict__.copy()
        for (key, val) in attributes.items():
            if hasattr(val, 'to_dict'):
                attributes[key] = val.to_dict()
                continue
            if 'time' in key:
                try:
                    attributes[key] = val.isoformat()
                    continue
                except (ValueError, AttributeError):
                    pass
            if 'amt' in key:
                try:
                    attributes[key] = Decimal(str(val)).quantize(Decimal('.0001'))  # Round to 4 DP
                    continue
                except (ValueError, AttributeError):
                    pass
        return attributes

    def to_json(self):
        return json.dumps(self, default=lambda o: default_convert_to_json(o))

    @classmethod
    def from_json(cls, json_string):
        try:
            attributes = json.loads(json_string)
        except JSONDecodeError as e:
            logging.error("Could not decode json: %s", json_string)
            raise e
        if not isinstance(attributes, dict):
            raise ValueError()
        return cls.from_dict(attributes)

    @classmethod
    def from_dict(cls, attributes: dict):
        if attributes is None:
            return
        obj = cls()
        attributes = attributes.copy()
        attributes = _convert_attributes(
            attributes, "time", datetime.datetime.fromisoformat
        )
        attributes = _convert_attributes(attributes, "amt", lambda x: float(x))
        obj.__dict__ = attributes
        obj.validate()
        return obj

    def validate(self):
        for (attribute, typ) in self.mandatory_attributes().items():
            val = self.__dict__.get(attribute)
            if not isinstance(val, typ):
                raise ValueError("%s is not of type %s" % (attribute, typ))

    def mandatory_attributes(self) -> dict:
        # should be overridden if there are mandatory attributes for deserialisation
        return {}


def default_convert_to_json(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, Serializable):
        return obj.to_dict()
    elif isinstance(obj, Enum):
        return obj.value
    else:
        return obj.__dict__.copy()


def _convert_attributes(attributes: dict, search: str, func) -> dict:
    for (key, val) in attributes.items():
        if search in key:
            try:
                time = func(val)
                attributes[key] = time
            except (ValueError, AttributeError, TypeError):
                pass
    return attributes
