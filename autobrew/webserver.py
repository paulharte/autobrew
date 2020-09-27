import logging

from flask import Flask, render_template, request, jsonify
from flask_googlecharts import GoogleCharts
from flask_injector import FlaskInjector
from injector import Injector, inject
from werkzeug.exceptions import abort

from autobrew.charts.make_chart import make_chart
from autobrew.dependencies import configure, autobrew_injector
from autobrew.heating.heat_control import HeatControl
from autobrew.measurement.measurementService import MeasurementService
from autobrew.smelloscope.smelloscope import Smelloscope
from autobrew.temperature.tempSourceFactory import TempSourceFactory

app = Flask(__name__)
charts = GoogleCharts(app)
logger = logging.getLogger("autobrew")


@app.route("/")
@inject
def brew_monitor(temperature_sources: TempSourceFactory, smelloscope: Smelloscope):
    current_temp_sources = temperature_sources.get_all_temp_sources()

    # TODO: make robust to smelloscope initialisation exceptions
    active_source_names = [source.get_name() for source in current_temp_sources] + [
        smelloscope.get_name()
    ]
    """## Pull historical and turn into chart"""
    historical_service = MeasurementService()
    for series in historical_service.get_all_series():
        if series.get_name() in active_source_names:
            charts.register(make_chart(series))

    return render_template(
        "main_template.html",
        temp_sources=current_temp_sources,
        smell_sources=[smelloscope],
    )


@app.route("/nickname", methods=["PUT"])
def set_nickname(measurement_service: MeasurementService):
    if not request.json or not "name" in request.json:
        abort(400)

    measurement = measurement_service.set_measurement_nickname(
        request.json["name"], request.json.get("nickname")
    )
    return jsonify(measurement), 201


@app.route("/heat_status", methods=["GET"])
def get_heat_status(heater: HeatControl):
    status = "ON" if heater.is_power_on() else "OFF"
    return jsonify(status), 201


@app.route("/set_primary", methods=["PUT"])
def set_primary(source_factory: TempSourceFactory):
    if not request.json or not "name" in request.json:
        abort(400)
    name = request.json.get("name")
    for source in source_factory.get_all_temp_sources():
        if source.get_name() == name:
            source.set_primary(True)
        else:
            source.set_primary(False)
    return jsonify(name), 201


# Setup Flask Injector, this has to happen AFTER routes are added

FlaskInjector(app=app, injector=autobrew_injector)


def run_webserver(debug=False):
    logger.info("Starting webserver")
    if debug:
        logger.info("Webserver debug set to on")
    app.run(debug=debug, use_reloader=debug, host="0.0.0.0", port=7070)


if __name__ == "__main__":
    run_webserver(True)
