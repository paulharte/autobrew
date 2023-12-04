from abc import ABC


@ABC
class AlcoholSensorBase:
    def setup_mcp(self):
        pass

    def get_voltage(self) -> float:
        pass
