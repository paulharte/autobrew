from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.heating.heat_switcher import HeatSwitcher
from autobrew.smelloscope.hardware_alcohol_sensor import HardwareAlcoholSensor
from test.heating.mock_heat_control import MockHeatSwitcher
from autobrew.smelloscope.smelloscope import Smelloscope
from autobrew.temperature.tempSourceFactory import (
    TempSourceFactory,
    ProbeTempSourceFactory,
)

from injector import singleton
import platform
import logging

from test.smelloscope.stubAlcoholSensor import StubAlcoholSensor
from test.temperature.mockTempSourceFactory import MockTempSourceFactory

logger = logging.getLogger(APP_LOGGING_NAME)


def configure(binder):
    if platform.system() == "Windows":
        logger.info("Running on Windows, using mock temperature and smell sources")
        configure_stubs(binder)
    else:
        logger.debug(
            "Not Running on Windows, using Raspberry Pi smell and temperature sources"
        )
        configure_real(binder)


def configure_real(binder):
    binder.bind(TempSourceFactory, to=ProbeTempSourceFactory, scope=singleton)


def configure_stubs(binder):
    binder.bind(TempSourceFactory, to=MockTempSourceFactory, scope=singleton)
    binder.bind(HardwareAlcoholSensor, to=StubAlcoholSensor, scope=singleton)
    binder.bind(HeatSwitcher, to=MockHeatSwitcher, scope=singleton)
