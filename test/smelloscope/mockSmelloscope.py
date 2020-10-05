import random

from autobrew.smelloscope.smelloscope import Smelloscope


class MockSmelloscope(Smelloscope):

    def get_alcohol_level(self):
        return 20.0 + (float(random.randint(0, 9)) / 10)
