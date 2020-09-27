import datetime

from autobrew.measurement.measurementSeries import MeasurementSeries
from flask_googlecharts import MaterialLineChart


def make_chart(series: MeasurementSeries):
    options = _make_options(series)

    chart = MaterialLineChart(series.get_name(), options=options)
    chart.add_column("datetime", "Time")
    chart.add_column("number", "Temperature")

    rows = []
    for measurement in series.get_measurements():
        rows.append([measurement.time, measurement.measurement_amt])

    chart.add_rows(rows)
    return chart


def _make_options(series: MeasurementSeries) -> dict:
    min_amt = series.get_min_amount() or 0.0
    max_amt = series.get_max_amount() or 0.0
    vertical_padding = 3.0
    return {
        "title": series.get_name(),
        "legend": {"position": "none"},
        "width": 900,
        "height": 500,
        "chartArea": {"width": "85%",},
        "vAxis": {
            "viewWindow": {
                "min": min_amt - vertical_padding,
                "max": max_amt + vertical_padding,
            },
            "gridlines": {
                "count": -1,
                "units": {
                    "days": {"format": ["MMM dd"]},
                    "hours": {"format": ["HH:mm", "ha"]},
                },
            },
            "minorGridlines": {
                "units": {
                    "hours": {"format": ["hh:mm:ss a", "ha"]},
                    "minutes": {"format": ["HH:mm a Z", ":mm"]},
                }
            },
        },
    }
