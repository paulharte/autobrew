import datetime
import json
from json import JSONDecodeError
import logging

from autobrew.brew_settings import APP_LOGGING_NAME

logger = logging.getLogger(APP_LOGGING_NAME)


class Serializable:
    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(
            self, default=lambda o: convert_to_json(o), sort_keys=True, indent=4
        )

    @classmethod
    def from_json(cls, json_string):
        try:
            attributes = json.loads(json_string)
        except JSONDecodeError as e:
            logger.error("Could not decode json: %s", json_string)
            raise e
        if not isinstance(attributes, dict):
            raise ValueError()
        return cls.from_dict(attributes)

    @classmethod
    def from_dict(cls, attributes: dict):
        if attributes is None:
            return
        obj = cls()
        for (key, val) in attributes.items():
            if "time" in key:
                try:
                    time = datetime.datetime.fromisoformat(val)
                    attributes[key] = time
                except ValueError:
                    pass
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
    else:
        return obj.__dict__
