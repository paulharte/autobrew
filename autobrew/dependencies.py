from autobrew.temperature.tempSourceFactory import (
    TempSourceFactory,
    ProbeTempSourceFactory,
)
from autobrew.temperature.test.mockTempSourceFactory import MockTempSourceFactory
from injector import singleton
import platform


def configure(binder):
    binder.bind(TempSourceFactory, to=getTempSourceFactoryClass(), scope=singleton)


def getTempSourceFactoryClass():
    """ We want to mock out the temperature probes on windows"""
    if platform.system() == "Windows":
        print("Running on Windows, using mock temperature sources")
        return MockTempSourceFactory
    else:
        print("Not Running on Windows")
        return ProbeTempSourceFactory
