from flask import Blueprint, render_template
from injector import inject

from autobrew.brew_settings import MAX_TEMP_C, MIN_TEMP_C
from autobrew.heating.heat_control import HeatControl
from autobrew.temperature.tempSourceFactory import TempSourceFactory

heat_blueprint = Blueprint("heat_status", __name__, url_prefix="/heat_status")


@heat_blueprint.route("/", methods=["GET"])
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


@heat_blueprint.route("/turn_on", methods=["GET"])
@inject
def turn_heat_on(heater: HeatControl, temp_factory: TempSourceFactory):
    heater.turn_on()
    return get_heat_status(heater, temp_factory)


@heat_blueprint.route("/turn_off", methods=["GET"])
@inject
def turn_heat_off(heater: HeatControl, temp_factory: TempSourceFactory):
    heater.turn_off()
    return get_heat_status(heater, temp_factory)