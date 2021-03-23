import datetime

from autobrew.aws.brew.brewRemote import Serializable


class MeasurementRemote(Serializable):
    def __init__(self):
        self.source_name: str
        self.time: datetime.datetime
        self.measurement_amt: float
