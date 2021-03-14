import logging

from flask import Flask, render_template, request, jsonify, url_for
import flask_googlecharts
from flask_injector import FlaskInjector
from injector import inject, Injector
from werkzeug.exceptions import abort, HTTPException
from werkzeug.utils import redirect

from autobrew.brew.brewEndpoints import brew_blueprint
from autobrew.brew.brewService import BrewService
from autobrew.brew_settings import APP_LOGGING_NAME, MAX_TEMP_C, MIN_TEMP_C
from autobrew.charts.make_chart import make_chart
from autobrew.configuration import configure
from autobrew.heating.heat_control import HeatControl
from autobrew.measurement.measurementService import MeasurementService
from autobrew.smelloscope.smelloscopeFactory import SmelloscopeFactory
from autobrew.temperature.tempSourceFactory import TempSourceFactory
from autobrew.utils.googlecharts_flask_patch_utils import prep_data

# Patch can be removed when this PR is merged
# https://github.com/wikkiewikkie/flask-googlecharts/pull/6
flask_googlecharts.utils.prep_data = prep_data

app = Flask(__name__)
charts = flask_googlecharts.GoogleCharts(app)
logger = logging.getLogger(APP_LOGGING_NAME)
app.register_blueprint(brew_blueprint)


@app.route("/", methods=["GET"])
@inject
def index(brew_service: BrewService):
    brew = brew_service.get_active()
    if not brew:
        return redirect(url_for("brews.view_brews"))
    return redirect(url_for("temperature_monitor"))


@app.route("/temperature_monitor", methods=["GET"])
@inject
def temperature_monitor(
    brew_service: BrewService,
    temperature_sources: TempSourceFactory,
    historical_service: MeasurementService,
):
    current_temp_sources = temperature_sources.get_all_temp_sources()
    active_source_names = [source.get_name() for source in current_temp_sources]
    brew = brew_service.get_active()
    if not brew:
        return render_template("error.html", message="No active brew")

    # Pull from historical and turn into chart
    for series in historical_service.get_all_series_for_brew(brew):
        if series.get_name() in active_source_names:
            charts.register(make_chart(series))

    return render_template("temperature.html", temp_sources=current_temp_sources)


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
def get_live_alcohol_level(smelloscopeFactory: SmelloscopeFactory):
    if not request.args or "name" not in request.args:
        abort(400)
    name = request.args.get("name")

    for smelloscope in smelloscopeFactory.get_all_sources():
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


@app.route("/alcohol_monitor", methods=["GET"])
@inject
def alcohol_level(
    brew_service: BrewService,
    smell_factory: SmelloscopeFactory,
    historical_service: MeasurementService,
):
    current_sources = smell_factory.get_all_sources()
    active_source_names = [source.get_name() for source in current_sources]
    brew = brew_service.get_active()
    if not brew:
        return render_template("error.html", message="No active brew")

    # Pull from historical and turn into chart
    for series in historical_service.get_all_series_for_brew(brew):
        if series.get_name() in active_source_names:
            charts.register(make_chart(series))

    return render_template("alcohol.html", smell_sources=current_sources)


@app.route("/nickname")
@inject
def set_nickname(
    source_factory: TempSourceFactory, smelloscopeFactory: SmelloscopeFactory
):
    if not request.args or "name" not in request.args or "nickname" not in request.args:
        abort(400)
    name = request.args.get("name")
    nickname = request.args.get("nickname")

    source = source_factory.get_temp_source(name)
    message = name + " successfully updated nickname to " + nickname

    if source:
        source.set_nickname(nickname)
        logger.info(message)
        return render_template("success.html", message=message)

    smelloscope = smelloscopeFactory.get_source(name)
    if smelloscope:
        smelloscope.set_nickname(nickname)
        logger.info(message)
        return render_template("success.html", message=message)

    return render_template("error.html", message="Could not find probe named: " + name)


@app.route("/heat_status", methods=["GET"])
@inject
def get_heat_status(heater: HeatControl, temp_factory: TempSourceFactory):
    status = "ON" if heater.is_power_on() else "OFF"
    primary_source = temp_factory.get_primary_source()
    return render_template(
        "heater_status.html",
        status=status,
        max=MAX_TEMP_C,
        min=MIN_TEMP_C,
        source=primary_source,
    )


@app.route("/config", methods=["GET"])
@inject
def config(source_factory: TempSourceFactory, smelloscopeFactory: SmelloscopeFactory):

    return render_template(
        "config.html",
        smell_sources=smelloscopeFactory.get_all_sources(),
        temp_sources=source_factory.get_all_temp_sources(),
    )


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
        logger.info(message)
        return render_template("success.html", message=message)
    else:
        message = "Could not find probe named: " + name
        logger.error(message)
        return render_template("error.html", message=message)


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    logger.exception(e)

    return render_template("error.html", e=str(e))


def run_webserver(injector: Injector, debug=False):
    logger.info("Starting webserver")
    FlaskInjector(app=app, injector=injector)
    if debug:
        logger.info("Webserver debug set to on")
    app.run(debug=debug, use_reloader=debug, host="0.0.0.0", port=7070)


if __name__ == "__main__":
    run_webserver(Injector([configure]), True)
