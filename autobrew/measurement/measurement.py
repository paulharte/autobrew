import datetime


class Measurement(object):
    def __init__(self, source: str, time: datetime.datetime, measurement_amt: float):
        self.source_name = source
        self.time = time
        self.measurement_amt = measurement_amt

    def __str__(self):
        return "%s - %s - %s" % (self.source_name, self.time, self.measurement_amt)

    def __eq__(self, other):
        return (
            (self.source_name == other.source_name)
            & (self.time == other.time)
            & (self.measurement_amt == other.measurement_amt)
        )
