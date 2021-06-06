import datetime
import json

from brew.brewRemote import Serializable


class MeasurementRemote(Serializable):
    def __init__(self):
        self.source_name: str
        self.time: datetime.datetime
        self.measurement_amt: float

    def mandatory_attributes(self) -> dict:
        return {"measurement_amt": float, "time": datetime.datetime}

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'source_name': self.source_name,
                           'time': self.time.isoformat(),
                           "measurement_amt": self.measurement_amt}

    @classmethod
    def from_dict(cls, attributes: dict):
        obj = cls()
        obj.source_name = attributes.get('source_name')
        obj.time = datetime.datetime.fromisoformat(attributes['time'])
        obj.measurement_amt = float(attributes.get('measurement_amt'))
        obj.validate()
        return obj


