from typing import List

from brew.brewRemote import Serializable
from measurements.measurementRemote import MeasurementRemote


class MeasurementSeriesRemote(Serializable):
    def __init__(self):
        self.source_name: str
        self.measurements: List[MeasurementRemote]
        self.brew_id: str
        self.brew_remote_id: str
        self.nickname: str = None

    def mandatory_attributes(self) -> dict:
        return {"source_name": str, "brew_remote_id": str, "measurements": list}

    @classmethod
    def from_dict(cls, attributes: dict):
        obj = Serializable.from_dict(attributes)
        obj.__class__ = cls
        obj.measurements = [MeasurementRemote.from_dict(meas) for meas in attributes['measurements']]
        return obj

    def to_dict(self):
        d = super().to_dict()
        d['measurements'] = [meas.to_dict() for meas in self.measurements]
        return d
