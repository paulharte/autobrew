from unittest import TestCase

from autobrew.brew.brew import Brew, sort_brews


class TestBrew(TestCase):
    def test_newbrew(self):
        brew1 = Brew("one")
        brew2 = Brew("two")
        brew3 = Brew("three")
        brew2.active = True
        brew1.active = False

        arr = sort_brews([brew1, brew2, brew3])
        self.assertEqual(
            "two", arr[0].name,
        )
