from autobrew.measurement.measurementSeries import MeasurementSeries
from flask_googlecharts import LineChart


def make_chart(series: MeasurementSeries):
    chart = LineChart(series.get_name())
    chart.add_column('datetime', 'Time')
    chart.add_column('number', 'Temperature')

    rows = []
    for measurement in series.measurements:
        rows.append([measurement.time, measurement.measurement_amt])

    chart.add_rows(rows)
    print(rows)

    return chart
