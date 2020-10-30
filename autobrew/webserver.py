import logging

from flask import Flask, render_template, request, jsonify
import flask_googlecharts
from flask_injector import FlaskInjector
from injector import inject
from werkzeug.exceptions import abort, HTTPException

from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.charts.make_chart import make_chart
from autobrew.dependencies import autobrew_injector
from autobrew.heating.heat_control import HeatControl
from autobrew.measurement.measurementService import MeasurementService
from autobrew.smelloscope.smelloscope import Smelloscope, SmelloscopeNotAvailable
from autobrew.temperature.tempSourceFactory import TempSourceFactory
from autobrew.utils.googlecharts_flask_patch_utils import prep_data

# Patch can be removed when this PR is merged
# https://github.com/wikkiewikkie/flask-googlecharts/pull/6
flask_googlecharts.utils.prep_data = prep_data

app = Flask(__name__)
charts = flask_googlecharts.GoogleCharts(app)
logger = logging.getLogger(APP_LOGGING_NAME)


@app.route("/", methods=["GET"])
@inject
def temperature_monitor(temperature_sources: TempSourceFactory):
    current_temp_sources = temperature_sources.get_all_temp_sources()
    active_source_names = [source.get_name() for source in current_temp_sources]

    """## Pull historical and turn into chart"""
    historical_service = MeasurementService()
    for series in historical_service.get_all_series():
        if series.get_name() in active_source_names:
            charts.register(make_chart(series))

    return render_template("main_template.html", temp_sources=current_temp_sources)


@app.route("/live_temperature", methods=["GET"])
@inject
def get_live_temp(temperature_sources: TempSourceFactory):
    if not request.args or "name" not in request.args:
        abort(400)
    name = request.args.get("name")
    current_temp_sources = temperature_sources.get_all_temp_sources()
    for source in current_temp_sources:
        if name == source.get_name():
            measurement = source.get_temperature_measurement()
            payload = {
                "temperature": measurement.measurement_amt,
                "time": measurement.time,
                "name": measurement.source_name,
            }
            return jsonify(payload)
    # If the name is not present, abort
    logger.error("Bad name: %s", name)
    abort(400)

@app.route("/live_alcohol_level", methods=["GET"])
@inject
def get_live_alcohol_level(smelloscope: Smelloscope):
    if not request.args or "name" not in request.args:
        abort(400)
    name = request.args.get("name")

    if name == smelloscope.get_name():
        measurement = smelloscope.get_measurement()
        payload = {
            "alcohol_level": measurement.measurement_amt,
            "time": measurement.time,
            "name": measurement.source_name,
        }
        return jsonify(payload)
    # If the name is not present, abort
    logger.error("Bad name: %s", name)
    abort(400)


@app.route("/alcohol_level", methods=["GET"])
@inject
def alcohol_level(smelloscope: Smelloscope):

    """## Pull historical and turn into chart"""
    historical_service = MeasurementService()
    try:
        series = historical_service.get_series(smelloscope.get_name())
        if series:
            charts.register(make_chart(series))
        return render_template("alcohol.html", smell_sources=[smelloscope])
    except SmelloscopeNotAvailable as e:
        logger.exception(e)
        return render_template(
            "error.html",
            message="Alcohol measurement not possible, as no sources found",
        )


@app.route("/nickname")
@inject
def set_nickname(source_factory: TempSourceFactory):
    if not request.args or "name" not in request.args or "nickname" not in request.args:
        abort(400)
    name = request.args.get("name")
    nickname = request.args.get("nickname")

    source = source_factory.get_temp_source(name)
    if not source:
        return render_template(
            "success.html", success_message="Could not find probe named: " + name
        )

    source.set_nickname(nickname)
    message = name + " successfully updated nickname to " + nickname
    logger.info(message)
    return render_template("success.html", success_message=message)


@app.route("/heat_status", methods=["GET"])
@inject
def get_heat_status(heater: HeatControl):
    status = "ON" if heater.is_power_on() else "OFF"
    message = "Heating status is: " + status
    return render_template("success.html", success_message=message)


@app.route("/config", methods=["GET"])
@inject
def config(source_factory: TempSourceFactory, smelloscope: Smelloscope):

    return render_template("config.html", smell_sources=[smelloscope], temp_sources=source_factory.get_all_temp_sources())


@app.route("/set_primary")
@inject
def set_primary(source_factory: TempSourceFactory):
    if not request.args or "name" not in request.args:
        abort(400)
    name = request.args.get("name")

    success = source_factory.set_primary_source(name)
    if success:
        message = (
            name
            + " successfully set as primary temperature source. Heat switching is enabled"
        )
    else:
        message = "Could not find probe named: " + name
    logger.info(message)
    return render_template("success.html", success_message=message)


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    logger.exception(e)

    return render_template("error.html", e=str(e))


# Setup Flask Injector, this has to happen AFTER routes are added
FlaskInjector(app=app, injector=autobrew_injector)


def run_webserver(debug=False):
    logger.info("Starting webserver")
    if debug:
        logger.info("Webserver debug set to on")
    app.run(debug=debug, use_reloader=debug, host="0.0.0.0", port=7070)


if __name__ == "__main__":
    run_webserver(True)
