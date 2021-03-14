from unittest import TestCase

from injector import Injector

from autobrew.brew.brewService import BrewService
from autobrew.configuration import configure_test
from autobrew.file.fileStorage import FileStorage


class TestBrewService(TestCase):
    def setUp(self) -> None:
        self.injector = Injector([configure_test])
        storage = self.injector.get(FileStorage)
        storage.clear_everything()

    def test_newbrew(self):
        service = self.injector.get(BrewService)
        brew = service.new("Prehistoric Pilsner")
        all_brews = service.get_all()
        self.assertIsNotNone(brew.id)
        self.assertIn(brew, all_brews)
        self.assertEqual(len(all_brews), 1)
        self.assertTrue(brew.active)

        brew2 = service.new("PorterSaurus")
        all_brews = service.get_all()
        self.assertEqual(len(all_brews), 2)
        active_brew = service.get_active()
        self.assertEqual(active_brew, brew2)
        self.assertTrue(active_brew.active)

        service.set_active(brew.id)

        all_brews = service.get_all()
        self.assertEqual(len(all_brews), 2)
        active_brew = service.get_active()
        self.assertEqual(active_brew, brew)
        self.assertTrue(active_brew.active)

        all_brews = service.get_all()
        self.assertEqual(len(all_brews), 2)
        count = 0
        for brew in all_brews:
            if brew.active:
                count += 1
        self.assertEqual(1, count)
