from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.heating.heat_control import HeatControl
from test.heating.mock_heat_control import MockHeatControl
from autobrew.smelloscope.smelloscope import Smelloscope
from test.smelloscope.mockSmelloscope import MockSmelloscope
from autobrew.temperature.tempSourceFactory import (
    TempSourceFactory,
    ProbeTempSourceFactory,
)

from injector import singleton, Injector
import platform
import logging

from test.temperature.mockTempSourceFactory import MockTempSourceFactory

logger = logging.getLogger(APP_LOGGING_NAME)


def configure(binder):
    binder.bind(TempSourceFactory, to=getTempSourceFactoryClass(), scope=singleton)
    binder.bind(Smelloscope, to=getSmellClass(), scope=singleton)
    binder.bind(HeatControl, to=getHeatClass(), scope=singleton)


def getTempSourceFactoryClass():
    """ We want to mock out the temperature probes on windows"""
    if platform.system() == "Windows":
        logger.info("Running on Windows, using mock temperature sources")
        return MockTempSourceFactory
    else:
        logger.debug("Not Running on Windows, using real probes")
        return ProbeTempSourceFactory


def getSmellClass():
    """ We want to mock out the temperature probes on windows"""
    if platform.system() == "Windows":
        logger.info("Running on Windows, using mock temperature sources")
        return MockSmelloscope
    else:
        logger.debug("Not Running on Windows, using real smelloscope")
        return Smelloscope


def getHeatClass():
    """ We want to mock out the temperature probes on windows"""
    if platform.system() == "Windows":
        logger.info("Running on Windows, using mock temperature sources")
        return MockHeatControl
    else:
        logger.debug("Not Running on Windows, using USD heat Control")
        return HeatControl


autobrew_injector = Injector([configure])
