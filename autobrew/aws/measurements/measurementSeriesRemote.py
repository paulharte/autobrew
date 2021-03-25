import logging
from json import JSONDecodeError
from typing import List

from autobrew.brew_settings import APP_LOGGING_NAME
from brew.brewRemote import Serializable
from measurements.measurementRemote import MeasurementRemote
import json

logger = logging.getLogger(APP_LOGGING_NAME)


class MeasurementSeriesRemote(Serializable):
    def __init__(self):
        self.source_name: str
        self.measurements: List[MeasurementRemote]
        self.brew_id: int
        self.brew_remote_id: str
        self.nickname: str = None

    def mandatory_attributes(self) -> dict:
        return {"source_name": str, "brew_remote_id": str, "measurements": list}

    @classmethod
    def from_json(cls, json_string):
        try:
            attributes = json.loads(json_string)
        except JSONDecodeError as e:
            logger.error("Could not decode json: %s", json_string)
            raise e
        if not isinstance(attributes, dict):
            raise ValueError()
        o = cls.from_dict(attributes)
        o.measurements = [MeasurementRemote.from_dict(meas) for meas in o.measurements]
        return o
