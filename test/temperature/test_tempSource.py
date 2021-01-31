from unittest import TestCase, mock

from injector import Injector

import autobrew.temperature.tempSource as tempSource
from autobrew.configuration import configure_test
from autobrew.temperature.probeTempApi import ProbeApi
from autobrew.temperature.tempSourceFactory import ProbeTempSourceFactory


class TestTempSource(TestCase):
    injector = Injector([configure_test])
    factory = injector.get(ProbeTempSourceFactory)

    def test_nickname(self):
        source = self.factory.get_temp_source("room")
        self.assertEqual(source.get_name(), tempSource.PROBE_PREFIX + "room")
        source.set_nickname("nick")
        self.assertEqual(source.get_display_name(), "nick")

    def test_filename(self):
        api = self.injector.get(ProbeApi)
        source2 = tempSource.TempSource(api, "path/to/a/filename2")
        self.assertEqual(source2.get_display_name(), tempSource.PROBE_PREFIX + "a")

        source3 = tempSource.TempSource(api, "/sys/bus/w1/devices/uniquename/w1_slave")
        self.assertEqual(
            source3.get_display_name(), tempSource.PROBE_PREFIX + "uniquename"
        )

        source4 = tempSource.TempSource(
            api, "sys/bus/w1/devices/28-041651652cff/w1_slave"
        )
        self.assertEqual(
            source4.get_display_name(), tempSource.PROBE_PREFIX + "28-041651652cff"
        )

    def test_equality(self):
        api = self.injector.get(ProbeApi)
        source1 = tempSource.TempSource(api, "path/to/a/filename2")
        source2 = tempSource.TempSource(api, "path/to/a/filename2")
        source1.set_primary(True)

        self.assertEqual(source1, source2)

    def test_temp(self):
        api = self.injector.get(ProbeApi)
        source1 = tempSource.TempSource(api, "brew")
        self.assertEqual(
            type(source1.get_temperature_measurement().measurement_amt), float
        )
