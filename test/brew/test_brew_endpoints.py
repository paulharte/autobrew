
from unittest import TestCase

from flask_injector import FlaskInjector
from injector import Injector

from autobrew.configuration import configure_test
from autobrew.webserver import app


class TestBrewWebserver(TestCase):
    def make_client(self):
        self.injector = Injector([configure_test])
        FlaskInjector(app=app, injector=self.injector)
        return app.test_client()

    def test_update_status(self):
        client = self.make_client()
        response = client.get("/brews/new?name=statusbrew")
        self.assertEqual(response.status_code, 200)

        response = client.get("/brews/0/status?stage=BOTTLE_CONDITIONING")
        self.assertEqual(response.status_code, 200)

        response = client.get("/brews/")
        self.assertIn("CONDITIONING", str(response.data))

        response = client.get("/brews/0/complete")
        self.assertEqual(response.status_code, 200)

        response = client.get("/brews/")
        self.assertIn("COMPLETE", str(response.data))


