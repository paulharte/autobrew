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


@app.route("/", methods=["GET"])
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


@app.route("/nickname")
@inject
def set_nickname(source_factory: TempSourceFactory):
    if not request.args or "name" not in request.args or 'nickname' not in request.args:
        abort(400)
    name = request.args.get("name")
    nickname = request.args.get("nickname")

    source = source_factory.get_temp_source(name)
    if not source:
        return render_template("success.html", success_message="Could not find probe named: " + name)

    source.set_nickname(nickname)
    message = name + " successfully updated nickname to " + nickname
    logger.info(message)
    return render_template("success.html", success_message=message)


@app.route("/heat_status", methods=["GET"])
@inject
def get_heat_status(heater: HeatControl):
    status = "ON" if heater.is_power_on() else "OFF"
    return jsonify(status), 201


@app.route("/set_primary")
@inject
def set_primary(source_factory: TempSourceFactory):
    if not request.args or "name" not in request.args:
        abort(400)
    name = request.args.get("name")

    success = source_factory.set_primary_source(name)
    if success:
        message = name + " successfully set as primary temperature source. Heat switching is enabled"
    else:
        message = "Could not find probe named: " + name
    logger.info(message)
    return render_template(
        "success.html",
        success_message=message
    )


# Setup Flask Injector, this has to happen AFTER routes are added

FlaskInjector(app=app, injector=autobrew_injector)


def run_webserver(debug=False):
    logger.info("Starting webserver")
    if debug:
        logger.info("Webserver debug set to on")
    app.run(debug=debug, use_reloader=debug, host="0.0.0.0", port=7070)


if __name__ == "__main__":
    run_webserver(True)
