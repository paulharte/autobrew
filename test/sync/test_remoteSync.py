from unittest import TestCase

from injector import Injector

from autobrew.configuration import configure_test
from autobrew.sync.awsConfig import AwsConfig
from autobrew.sync.identityManger import IdentityManager
from autobrew.sync.remoteSync import RemoteSync


class TestRemoteSync(TestCase):
    def setUp(self) -> None:
        self.injector = Injector([configure_test])
        identity = self.injector.get(IdentityManager)
        self.sync = RemoteSync(identity, AwsConfig('uat'))

    def test_formMeasurementUrl(self):
        url = self.sync.formMeasurementUrl('brew1', 'temp1')
        self.assertEqual('https://brew-uat.paulspetprojects.net/brew/brew1/measurements/temp1', url)

    def test_formBrewUrl(self):
        url = self.sync.formBrewUrl('brew1')
        self.assertEqual('https://brew-uat.paulspetprojects.net/brew/brew1', url)
