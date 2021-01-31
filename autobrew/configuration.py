from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.heating.heat_switcher import HeatSwitcher
from autobrew.measurement.fileStorage import FileStorage
from autobrew.smelloscope.hardware_alcohol_sensor import HardwareAlcoholSensor
from autobrew.temperature.probeTempApi import ProbeApi
from test.heating.mock_heat_control import MockHeatSwitcher
from autobrew.temperature.tempSourceFactory import (
    TempSourceFactory,
    ProbeTempSourceFactory,
)

from injector import singleton
import platform
import logging

from test.measurement.stubFileStorage import StubFileStorage
from test.smelloscope.stubAlcoholSensor import StubAlcoholSensor
from test.temperature.mockTempSourceFactory import MockTempSourceFactory
from test.temperature.stubProbeApi import StubProbeApi

logger = logging.getLogger(APP_LOGGING_NAME)


def configure(binder):
    if platform.system() == "Windows":
        logger.info("Running on Windows, using mock temperature and smell sources")
        configure_local(binder)
    else:
        logger.debug(
            "Not Running on Windows, using Raspberry Pi smell and temperature sources"
        )
        configure_prod(binder)


def configure_prod(binder):
    binder.bind(TempSourceFactory, to=ProbeTempSourceFactory, scope=singleton)
    binder.bind(ProbeApi, to=ProbeApi, scope=singleton)
    binder.bind(FileStorage, to=FileStorage, scope=singleton)


def configure_local(binder):
    binder.bind(TempSourceFactory, to=ProbeTempSourceFactory, scope=singleton)
    binder.bind(HardwareAlcoholSensor, to=StubAlcoholSensor, scope=singleton)
    binder.bind(HeatSwitcher, to=MockHeatSwitcher, scope=singleton)
    binder.bind(ProbeApi, to=StubProbeApi, scope=singleton)


def configure_test(binder):
    configure_local(binder)
    binder.bind(FileStorage, to=StubFileStorage, scope=singleton)
