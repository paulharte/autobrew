from typing import List

from autobrew.aws.brew.brewRemote import Serializable
from autobrew.aws.measurements.measurementRemote import MeasurementRemote
import json


class MeasurementSeriesRemote(Serializable):
    def __init__(self):
        self.source_name: str
        self.measurements: List[MeasurementRemote]
        self.brew_id: int
        self.brew_remote_id: str
        self.nickname: str = None

    @classmethod
    def from_json(cls, json_string):
        attributes = json.loads(json_string)
        if not isinstance(attributes, dict):
            raise ValueError
        o = cls.from_dict(attributes)
        o.measurements = [MeasurementRemote.from_dict(meas) for meas in o.measurements]
        return o
