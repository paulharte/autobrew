import datetime
import json
import logging
from decimal import Decimal
from json import JSONDecodeError


class Serializable:
    def to_dict(self):
        attributes = self.__dict__
        attributes = _convert_attributes(attributes, 'time', lambda x: x.isoformat())
        return _convert_attributes(attributes, 'amt', lambda x: Decimal(x))

    def to_json(self):
        d = self.to_dict()
        return json.dumps(
            d, default=lambda o: convert_to_json(o), sort_keys=True, indent=4
        )

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
        attributes = _convert_attributes(attributes, 'time', datetime.datetime.fromisoformat)
        attributes =  _convert_attributes(attributes, 'amt', lambda x: float(x))
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


def convert_to_json(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj.__dict__


def _convert_attributes(attributes: dict, search: str, func) -> dict:
    for (key, val) in attributes.items():
        if search in key:
            try:
                time = func(val)
                attributes[key] = time
            except (ValueError, AttributeError):
                pass
    return attributes