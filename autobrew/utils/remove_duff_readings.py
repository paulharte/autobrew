from autobrew.measurement.measurementService import MeasurementService

service = MeasurementService()

for series in service.get_all_series_for_brew():
    for measurement in series.get_measurements():
        if measurement.measurement_amt > 40.5:
            series.measurements.remove(measurement)
            print("measurement removed:" + str(measurement))
            service.save_series(series)
