import datetime


class Measurement(object):

    source_name: str = None
    time: datetime.datetime = None
    measurement_amt: float = None

    def __init__(self, source: str, time: datetime.datetime, measurement_amt: float):
        self.source_name = source
        self.time = time
        self.measurement_amt = measurement_amt

    def __str__(self):
        return '%s - %s - %s' % (self.source_name, self.time, self.measurement_amt)