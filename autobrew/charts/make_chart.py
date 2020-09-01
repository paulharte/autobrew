import datetime

from autobrew.measurement.measurementSeries import MeasurementSeries
from flask_googlecharts import LineChart


def make_chart(series: MeasurementSeries):
    options = _make_options(series)

    chart = LineChart(series.get_name(), options=options)
    chart.add_column("datetime", "Time")
    chart.add_column("number", "Temperature")

    rows = []
    for measurement in series.measurements:
        rows.append([measurement.time, measurement.measurement_amt])

    chart.add_rows(rows)

    return chart

def _make_options(series: MeasurementSeries) -> dict:
    return {
        'title': series.get_name(),
        'legend': {'position': 'none'},
        'chartArea': {
            'width': '85%'
        },
        'hAxis': {
            'viewWindow': {
                # 'min': datetime.datetime(2014, 11, 31, 18),
                # 'max': new Date(2015, 0, 3, 1)
        },
        'gridlines': {
            'count': -1,
            'units': {
                'days': {'format': ['MMM dd']},
                'hours': {'format': ['HH:mm', 'ha']},
            }
        },
        'minorGridlines': {
            'units': {
                'hours': {'format': ['hh:mm:ss a', 'ha']},
                'minutes': {'format': ['HH:mm a Z', ':mm']}
            }
        }
    }
    }
