from autobrew.smelloscope.smelloscope import Smelloscope
from autobrew.smelloscope.test.mockSmelloscope import MockSmelloscope
from autobrew.temperature.tempSourceFactory import (
    TempSourceFactory,
    ProbeTempSourceFactory,
)
from autobrew.temperature.test.mockTempSourceFactory import MockTempSourceFactory
from injector import singleton
import platform
import logging

logger = logging.getLogger("autobrew")


def configure(binder):
    binder.bind(TempSourceFactory, to=getTempSourceFactoryClass(), scope=singleton)
    binder.bind(Smelloscope, to=getSmellClass(), scope=singleton)

def getTempSourceFactoryClass():
    """ We want to mock out the temperature probes on windows"""
    if platform.system() == "Windows":
        logger.info("Running on Windows, using mock temperature sources")
        return MockTempSourceFactory
    else:
        logger.debug("Not Running on Windows")
        return ProbeTempSourceFactory


def getSmellClass():
    """ We want to mock out the temperature probes on windows"""
    if platform.system() == "Windows":
        logger.info("Running on Windows, using mock temperature sources")
        return MockSmelloscope
    else:
        logger.debug("Not Running on Windows")
        return Smelloscope