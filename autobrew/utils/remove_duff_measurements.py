from injector import Injector

from autobrew.brew.brew import Brew
from autobrew.brew.brewService import BrewService
from autobrew.configuration import configure_prod, configure_local
from autobrew.measurement.measurementService import MeasurementService
from autobrew.measurement.seriesType import SeriesType

injector = Injector([configure_local])

def remove_duff_temperature_measurements(brew: Brew):
    service = injector.get(MeasurementService)
    series_array = service.get_all_series_for_brew(brew)
    for series in series_array:
        if series.type == SeriesType.TEMPERATURE:
            for measurement in series.get_measurements():
                if measurement.measurement_amt > 50.0:
                    series.measurements.remove(measurement)
                    service.save_series(series)
                    print("measurement removed: %s" % measurement)


def run():
    brew_service = injector.get(BrewService)
    active = brew_service.get_active()
    if active:
        remove_duff_temperature_measurements(active)
    else:
        raise Exception('No active brew!')

    print("Done!")

run()