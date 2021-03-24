from unittest import mock

from autobrew.alerting.tweeter.twitterAlerts import TwitterAlerter
from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.heating.heat_switcher import HeatSwitcher
from autobrew.file.fileStorage import FileStorage
from autobrew.smelloscope.hardware_alcohol_sensor import HardwareAlcoholSensor
from autobrew.sync.awsConfig import AwsConfig
from autobrew.sync.identityManger import IdentityManager
from autobrew.sync.remoteSync import RemoteSync
from autobrew.temperature.probeTempApi import ProbeApi
from test.alerting.StubTwitterAlerter import StubTwitterAlerter
from test.heating.mock_heat_control import MockHeatSwitcher
from autobrew.temperature.tempSourceFactory import (
    TempSourceFactory,
    ProbeTempSourceFactory,
)

from injector import singleton
import platform
import logging

from test.file.stubFileStorage import StubFileStorage
from test.smelloscope.stubAlcoholSensor import StubAlcoholSensor
from test.sync.stubIdentityManager import StubIdentityManager
from test.sync.stubRemoteSync import StubRemoteSync
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
    binder.bind(AwsConfig, to=AwsConfig("prod"), scope=singleton)


def configure_local(binder):
    binder.bind(TempSourceFactory, to=ProbeTempSourceFactory, scope=singleton)
    binder.bind(HardwareAlcoholSensor, to=StubAlcoholSensor, scope=singleton)
    binder.bind(HeatSwitcher, to=MockHeatSwitcher, scope=singleton)
    binder.bind(ProbeApi, to=StubProbeApi, scope=singleton)
    binder.bind(TwitterAlerter, to=StubTwitterAlerter, scope=singleton)
    binder.bind(AwsConfig, to=AwsConfig("uat"), scope=singleton)


def configure_test(binder):
    configure_local(binder)
    binder.bind(FileStorage, to=StubFileStorage, scope=singleton)
    binder.bind(IdentityManager, to=StubIdentityManager, scope=singleton)
    binder.bind(AwsConfig, to=mock.Mock(), scope=singleton)
    binder.bind(RemoteSync, to=StubRemoteSync, scope=singleton)
