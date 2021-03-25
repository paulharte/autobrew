import datetime

from brew.brewRemote import Serializable


class MeasurementRemote(Serializable):
    def __init__(self):
        self.source_name: str
        self.time: datetime.datetime
        self.measurement_amt: float

    def mandatory_attributes(self) -> dict:
        return {"measurement_amt": float, "time": datetime.datetime}
