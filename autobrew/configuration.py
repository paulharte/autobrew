from unittest import mock

from autobrew.alerting.tweeter.secretsService import extract_secrets
from autobrew.alerting.tweeter.twitterAlerts import TwitterAlerter
from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.heating.heat_control import HeatControl
from autobrew.heating.heat_switcher import HeatSwitcher
from autobrew.file.fileStorage import FileStorage
from autobrew.smelloscope.alcohol_sensor_base import AlcoholSensorBase
from autobrew.sync.awsConfig import AwsConfig
from autobrew.sync.cachedIdentityManager import CachedIdentityManger
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


def configure_prod(binder):
    # we import here to avoid importing these files in non-linux systems
    from autobrew.smelloscope.hardware_alcohol_sensor import HardwareAlcoholSensor

    if platform.system() == "Windows":
        logger.info(
            "Running on Windows, using local config instead (mock temperature and smell sources)"
        )
        configure_uat(binder)
        return
    logger.info("Running against PROD aws instance")
    binder.bind(TempSourceFactory, to=ProbeTempSourceFactory, scope=singleton)
    binder.bind(ProbeApi, to=ProbeApi, scope=singleton)
    binder.bind(AlcoholSensorBase, to=HardwareAlcoholSensor, scope=singleton)
    binder.bind(HeatControl, to=HeatControl, scope=singleton)
    binder.bind(FileStorage, to=FileStorage, scope=singleton)
    binder.bind(TwitterAlerter, to=TwitterAlerter(extract_secrets()), scope=singleton)
    binder.bind(AwsConfig, to=AwsConfig("prod"), scope=singleton)
    binder.bind(CachedIdentityManger, to=CachedIdentityManger, scope=singleton)


def configure_uat(binder):
    logger.info("Running against UAT aws instance")
    binder.bind(TempSourceFactory, to=ProbeTempSourceFactory, scope=singleton)
    binder.bind(AlcoholSensorBase, to=StubAlcoholSensor, scope=singleton)
    binder.bind(HeatSwitcher, to=MockHeatSwitcher, scope=singleton)
    binder.bind(HeatControl, to=HeatControl, scope=singleton)
    binder.bind(ProbeApi, to=StubProbeApi, scope=singleton)
    binder.bind(TwitterAlerter, to=StubTwitterAlerter, scope=singleton)
    binder.bind(AwsConfig, to=AwsConfig("uat"), scope=singleton)
    binder.bind(CachedIdentityManger, to=CachedIdentityManger, scope=singleton)


def configure_test(binder):
    binder.bind(TempSourceFactory, to=ProbeTempSourceFactory, scope=singleton)
    binder.bind(AlcoholSensorBase, to=StubAlcoholSensor, scope=singleton)
    binder.bind(HeatSwitcher, to=MockHeatSwitcher, scope=singleton)
    binder.bind(HeatControl, to=HeatControl, scope=singleton)
    binder.bind(ProbeApi, to=StubProbeApi, scope=singleton)
    binder.bind(TwitterAlerter, to=StubTwitterAlerter, scope=singleton)
    binder.bind(CachedIdentityManger, to=CachedIdentityManger, scope=singleton)
    binder.bind(FileStorage, to=StubFileStorage, scope=singleton)
    binder.bind(IdentityManager, to=StubIdentityManager, scope=singleton)
    binder.bind(AwsConfig, to=mock.Mock(), scope=singleton)
    binder.bind(RemoteSync, to=StubRemoteSync, scope=singleton)
