import time

from autobrew.dependencies import getTempSourceFactoryClass
from autobrew.measurement.measurementService import MeasurementService

SAMPLE_INTERVAL_SECONDS = 20


def run():
    measurement_service = MeasurementService()
    temp_factory = getTempSourceFactoryClass()()
    for iteration in range(0, 10):
        for source in temp_factory.get_all_temp_sources():
            measurement = source.get_temperature_measurement()
            measurement_service.save_measurement(measurement)
            print("Temperature measurement taken: " + str(measurement))
        time.sleep(SAMPLE_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
