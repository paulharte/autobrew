from unittest import TestCase

from flask_injector import FlaskInjector
from injector import Injector

from autobrew.brew.brewService import BrewService
from autobrew.configuration import configure_test
from autobrew.heating.heat_control import HeatControl
from autobrew.measurement.measurementService import MeasurementService
from autobrew.measurement.seriesType import SeriesType
from autobrew.smelloscope.smelloscope import Smelloscope
from autobrew.temperature.tempSource import PROBE_PREFIX
from autobrew.webserver import app
from test.temperature.stubProbeApi import STUB_BREW_TEMP_NAME


class TestWebserver(TestCase):
    def make_client(self):
        self.injector = Injector([configure_test])
        FlaskInjector(app=app, injector=self.injector)
        return app.test_client()

    def test_get(self):
        client = self.make_client()

        response = client.get("/")
        self.assertEqual(response.status_code, 302)

        response = client.get("/temperature_monitor")
        self.assertEqual(response.status_code, 200)

        response = client.get("/config")
        self.assertEqual(response.status_code, 200)

        response = client.get("/brews/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/heat_status")
        self.assertEqual(response.status_code, 200)
        self.assertIn( "Heater Status" , str(response.data))

    def test_heating(self):
        client = self.make_client()
        response = client.get("/heat_status/turn_off")
        self.assertEqual(response.status_code, 200)
        self.assertIn( "Heater Status" , str(response.data))

        heater = self.injector.get(HeatControl)
        self.assertFalse(heater.is_power_on())

        response = client.get("/heat_status/turn_on")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Heater Status", str(response.data))

        heater = self.injector.get(HeatControl)
        self.assertTrue(heater.is_power_on())


    def test_get_measurements(self):
        client = self.make_client()
        self._test_get_measurements(client)

    def test_new_brew(self):
        client = self.make_client()
        response = client.get("/brews/new?name=mynewbrew")
        self.assertEqual( response.status_code, 200)
        self.assertIn( "mynewbrew" , str(response.data))

        self._test_get_measurements(client)

    def _test_get_measurements(self, client):
        response = client.get("/live_alcohol_level")
        self.assertEqual(response.status_code, 400)

        response = client.get("/live_temperature")
        self.assertEqual(response.status_code, 400)

        response = client.get("/live_alcohol_level?name=" + Smelloscope.NAME)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alcohol_level", response.data)
        self.assertIn(b"name", response.data)
        self.assertIn(b"time", response.data)

        response = client.get("/live_temperature?name=" + PROBE_PREFIX + STUB_BREW_TEMP_NAME)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"temperature", response.data)
        self.assertIn(b"name", response.data)
        self.assertIn(b"time", response.data)

    def test_nickname(self):
        client = self.make_client()

        source_name = PROBE_PREFIX + STUB_BREW_TEMP_NAME

        meas_service = self.injector.get(MeasurementService)
        brew_service = self.injector.get(BrewService)
        response = client.get("/brews/new?name=mynewbrew")
        self.assertEqual(response.status_code, 200)
        series = meas_service.new_series(brew_service.get_active(), source_name, SeriesType.TEMPERATURE)

        response = client.get(
            "/nickname?name=" + PROBE_PREFIX + STUB_BREW_TEMP_NAME + "&nickname=my_nickname"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn( "successfully updated nickname to my_nickname" , str(response.data))

        response = client.get("/temperature_monitor")
        self.assertEqual(response.status_code, 200)
        self.assertIn( "my_nickname" , str(response.data))

    def test_primary(self):
        client = self.make_client()

        response = client.get("/set_primary?name=" + PROBE_PREFIX + STUB_BREW_TEMP_NAME)
        self.assertEqual(response.status_code, 200)
        self.assertIn( "successfully set as primary temperature source" , str(response.data))

    def test_heat_status(self):
        client = self.make_client()
        response = client.get("/heat_status")
        self.assertEqual(response.status_code, 200)
