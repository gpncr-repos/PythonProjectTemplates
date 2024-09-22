{% if cookiecutter.api_architecture == "grpc" %}
import abc


class IndexService(abc.ABC):
    """
    Базовый класс сервиса для получения общей информации о приложении
    """

    def GetInfo(self, *args, **kwargs) -> any:
        """
        Получить общую информацию о приложении
        """

        raise NotImplementedError
{% endif %}
