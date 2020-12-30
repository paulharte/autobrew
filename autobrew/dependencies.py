from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.heating.heat_control import HeatControl
from test.heating.mock_heat_control import MockHeatControl
from autobrew.smelloscope.smelloscope import Smelloscope
from test.smelloscope.mockSmelloscope import MockSmelloscope
from autobrew.temperature.tempSourceFactory import (
    TempSourceFactory,
    ProbeTempSourceFactory,
)

from injector import singleton
import platform
import logging

from test.temperature.mockTempSourceFactory import MockTempSourceFactory

logger = logging.getLogger(APP_LOGGING_NAME)


def configure(binder):
    if platform.system() == "Windows":
        logger.info("Running on Windows, using mock temperature and smell sources")
        configure_mocks(binder)
    else:
        logger.debug( "Not Running on Windows, using Raspberry Pi smell and temperature sources" )
        configure_real(binder)


def configure_real(binder):
    binder.bind(TempSourceFactory, to=ProbeTempSourceFactory, scope=singleton)
    binder.bind(Smelloscope, to=Smelloscope, scope=singleton)
    binder.bind(HeatControl, to=HeatControl, scope=singleton)


def configure_mocks(binder):
    binder.bind(TempSourceFactory, to=MockTempSourceFactory, scope=singleton)
    binder.bind(Smelloscope, to=MockSmelloscope, scope=singleton)
    binder.bind(HeatControl, to=MockHeatControl, scope=singleton)
