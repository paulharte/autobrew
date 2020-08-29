from flask import Flask, render_template, request, jsonify
from flask_googlecharts import GoogleCharts
from flask_injector import FlaskInjector
from injector import inject
from werkzeug.exceptions import abort

from autobrew.charts.make_chart import make_chart
from autobrew.dependencies import configure
from autobrew.measurement.measurementService import MeasurementService
from autobrew.temperature.tempSourceFactory import TempSourceFactory

app = Flask(__name__)
app.debug = True
charts = GoogleCharts(app)


@app.route("/")
@inject
def brew_monitor(temperature_sources: TempSourceFactory):
    current_temp_sources = temperature_sources.get_all_temp_sources()

    '''## Pull historical and turn into chart'''
    historical_service = MeasurementService()
    for series in historical_service.get_all_series():
        charts.register(make_chart(series))

    return render_template("main_template.html", temp_sources=current_temp_sources)


@app.route("/todo/api/v1.0/tasks", methods=["PUT"])
def set_nickname():
    if not request.json or not "name" in request.json:
        abort(400)

    measurement = MeasurementService().set_measurement_nickname(
        request.json["name"], request.json.get("nickname")
    )
    return jsonify(measurement), 201


# Setup Flask Injector, this has to happen AFTER routes are added
FlaskInjector(app=app, modules=[configure])

if __name__ == "__main__":
    app.run()
