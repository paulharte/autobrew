from unittest import TestCase, mock

import autobrew.temperature.tempSource as tempSource


class TestTempSource(TestCase):
    def test_nickname(self):
        source = tempSource.TempSource("filename")
        self.assertEqual(source.get_name(), tempSource.PROBE_PREFIX + "filename")
        source.set_nickname("nick")
        self.assertEqual(source.get_display_name(), "nick")

    def test_filename(self):
        source2 = tempSource.TempSource("path/to/a/filename2")
        self.assertEqual(source2.get_display_name(), tempSource.PROBE_PREFIX + "a")

        source3 = tempSource.TempSource("/sys/bus/w1/devices/uniquename/w1_slave")
        self.assertEqual(
            source3.get_display_name(), tempSource.PROBE_PREFIX + "uniquename"
        )

        source4 = tempSource.TempSource("sys/bus/w1/devices/28-041651652cff/w1_slave")
        self.assertEqual(
            source4.get_display_name(), tempSource.PROBE_PREFIX + "28-041651652cff"
        )

    def test_equality(self):
        source1 = tempSource.TempSource("path/to/a/filename2")
        source2 = tempSource.TempSource("path/to/a/filename2")
        source1.set_primary(True)

        self.assertEqual(source1, source2)

    def test_temp(self):
        with mock.patch(
            "test.temperature.test_tempSource.tempSource.read_temp", return_value=20.0
        ):
            source1 = tempSource.TempSource("path/to/a/filename2")
            self.assertEqual(
                source1.get_temperature_measurement().measurement_amt, 20.0
            )
