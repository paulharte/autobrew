import os
from typing import List


from storage.dynamo import Dynamo
from measurements.measurementSeriesRemote import MeasurementSeriesRemote

MEASUREMENT_SERIES_DYNAMO_TABLE = os.environ.get('measurement_table', default="autobrew_measurement_series")
MEASUREMENT_SERIES_KEY = ["brew_remote_id", "source_name"]


class MeasurementServiceRemote(object):
    def __init__(self, dynamo: Dynamo):
        self.db = dynamo

    def getAll(self) -> List[MeasurementSeriesRemote]:
        return [
            MeasurementSeriesRemote.from_dict(json_brew)
            for json_brew in self.db.get_all(MEASUREMENT_SERIES_DYNAMO_TABLE)
        ]

    def put(self, measurement_series: MeasurementSeriesRemote):
        self.db.put(MEASUREMENT_SERIES_DYNAMO_TABLE, measurement_series.to_dict())


    def get(self, brew_remote_id: str, source_name: str) -> MeasurementSeriesRemote:
        brew_dict = self.db.get(
            MEASUREMENT_SERIES_DYNAMO_TABLE,
            [brew_remote_id, source_name],
            MEASUREMENT_SERIES_KEY,
        )
        return MeasurementSeriesRemote.from_dict(brew_dict)

    def get_all_for_brew(self, brew_remote_id: str):
        json_series = self.db.get_many(
            MEASUREMENT_SERIES_DYNAMO_TABLE, brew_remote_id, MEASUREMENT_SERIES_KEY[0],
        )
        return [MeasurementSeriesRemote.from_dict(json_s) for json_s in json_series]

    def create(self, brew: MeasurementSeriesRemote):
        self.put(brew)

    def delete(self, brew_remote_id: str, source_name: str):
        self.db.delete(
            MEASUREMENT_SERIES_DYNAMO_TABLE,
            [brew_remote_id, source_name],
            MEASUREMENT_SERIES_KEY,
        )


def make_measurement_service() -> MeasurementServiceRemote:
    return MeasurementServiceRemote(Dynamo())
