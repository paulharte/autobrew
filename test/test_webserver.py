from unittest import TestCase

from flask_injector import FlaskInjector
from injector import Injector

from autobrew.configuration import configure_test
from autobrew.smelloscope.smelloscope import Smelloscope
from autobrew.temperature.tempSource import PROBE_PREFIX
from autobrew.webserver import app
from test.temperature.stubProbeApi import STUB_BREW_NAME


class TestWebserver(TestCase):
    def make_client(self):
        injector = Injector([configure_test])
        FlaskInjector(app=app, injector=injector)
        return app.test_client()

    def test_get(self):
        client = self.make_client()

        response = client.get("/")
        assert response.status_code == 200

        response = client.get("/config")
        assert response.status_code == 200

        response = client.get("/config")
        assert response.status_code == 200

        response = client.get("/live_alcohol_level")
        assert response.status_code == 400

        response = client.get("/live_temperature")
        assert response.status_code == 400

        response = client.get("/live_alcohol_level?name=" + Smelloscope.NAME)
        assert response.status_code == 200
        assert b"alcohol_level" in response.data
        assert b"name" in response.data
        assert b"time" in response.data

        response = client.get("/live_temperature?name=" + PROBE_PREFIX + STUB_BREW_NAME)
        assert response.status_code == 200
        assert b"temperature" in response.data
        assert b"name" in response.data
        assert b"time" in response.data

    def test_nickname(self):
        client = self.make_client()

        response = client.get(
            "/nickname?name=" + PROBE_PREFIX + STUB_BREW_NAME + "&nickname=my_nickname"
        )
        assert response.status_code == 200
        assert "successfully updated nickname to my_nickname" in str(response.data)

    def test_primary(self):
        client = self.make_client()

        response = client.get("/set_primary?name=" + PROBE_PREFIX + STUB_BREW_NAME)
        assert response.status_code == 200
        assert "successfully set as primary temperature source" in str(response.data)

    def test_heat_status(self):
        client = self.make_client()
        response = client.get("/heat_status")
        assert response.status_code == 200
