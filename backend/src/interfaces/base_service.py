import abc


class BaseOilRateCalculatorService(abc.ABC):
    """
    Базовый класс сервиса расчета дебита нефти
    """

    @abc.abstractmethod
    def calc_oil_rate(self, *args, **kwargs) -> None:
        """
        Рассчитать дебит нефти
        """

        raise NotImplementedError
