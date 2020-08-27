import pickle
from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries


class MeasurementStorage(object):
    """ Handles all file io for measurement series"""

    SUFFIX = ".storage"
    name: str = None

    def __init__(self, name: str):
        self.name = name.replace(self.SUFFIX, "")

    def add_measurement(self, measurement: Measurement):
        file, data = self._get_file_data()
        data.append(measurement)
        pickle.dump(data, file)
        # close the file
        file.close()

    def set_series(self, series: MeasurementSeries):
        file, data = self._get_file_data()
        data = series
        pickle.dump(data, file)
        # close the file
        file.close()

    def read(self) -> MeasurementSeries:
        file, data = self._get_file_data()
        file.close()
        return data

    def _get_file_data(self) -> (object, []):
        try:
            file = open(self.name + self.SUFFIX, "rb")
            data = pickle.load(file)
        except FileNotFoundError:
            file = open(self.name, "wb")
            data = MeasurementSeries(self.name)
        return file, data
