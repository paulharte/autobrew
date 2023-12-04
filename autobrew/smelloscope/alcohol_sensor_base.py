import abc


class AlcoholSensorBase(abc.ABC):
    @abc.abstractmethod
    def setup_mcp(self):
        pass

    @abc.abstractmethod
    def get_voltage(self) -> float:
        pass
