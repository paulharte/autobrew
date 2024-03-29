import logging
from typing import List

from injector import inject

from autobrew.brew.brewExceptions import AutobrewNotFoundError
from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.file.fileStorage import FileStorage
from autobrew.measurement.measurementSeries import MeasurementSeries

logger = logging.getLogger(APP_LOGGING_NAME)


class MeasurementStorage(object):
    """Handles all file io for measurement series"""

    SUB_FOLDER = "measurements"
    SUFFIX = ".txt"

    @inject
    def __init__(self, file_storage: FileStorage):
        self.file_storage = file_storage

    def read(self, series_id: str) -> MeasurementSeries:
        filename = self.form_filename(series_id)
        return self.file_storage.read(filename, self.SUB_FOLDER)

    def read_by_source(self, source_name: str, brew_id: str) -> MeasurementSeries:
        all_series = self.get_all_series()
        for series in all_series:
            if (series.source_name == source_name) and (series.brew_id == brew_id):
                return series

    def save(self, series: MeasurementSeries):
        filename = self.form_filename(series.id)
        self.file_storage.save(filename, series, self.SUB_FOLDER)

    def form_filename(self, series_id: str):
        return series_id + self.SUFFIX

    def get_all_series(self) -> List[MeasurementSeries]:
        filenames = self.file_storage.get_storage_files(
            suffix=self.SUFFIX, sub_folder=self.SUB_FOLDER
        )
        measurements = []
        for filename in filenames:
            try:
                series = self.file_storage.read(filename, self.SUB_FOLDER)
                measurements.append(series)
            except AutobrewNotFoundError as e:
                logger.exception(e)
        return measurements
