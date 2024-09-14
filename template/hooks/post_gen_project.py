import dataclasses
import pathlib
import sys
import textwrap


@dataclasses.dataclass
class Config:
    """
    Конфиг пост-хука
    """

    # Путь к папке src шаблона
    template_path = pathlib.Path.cwd().resolve().parent / "{{ cookiecutter.service_name }}" / "src"


class DependenciesCreator:
    """
    Класс, содержащий список используемых зависимостей в шаблонизаторе
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        # шаблон pyproject.toml
        self.pyproject_template = textwrap.dedent(
            """\
                [tool.poetry]
                name = "{{ cookiecutter.service_name }}"
                version = "0.1.0"
                description = ""
                authors = ["gpn_team"]
                readme = "README.md"

                [build-system]
                requires = ["poetry-core"]
                build-backend = "poetry.core.masonry.api"

                [tool.poetry.dependencies]
                python = "^3.11"
                fastapi = "^0.114.0"
            """
        )

        # словарь зависимостей, где ключ - название библиотеки / фреймворка, значение - версия
        self.dependencies = {
            "uvicorn": "^0.30.6",
            "pydantic-settings": "^2.5.0",
            "dependency-injector": "^4.41.0"
        }

    def remove_dependency(self, name: str) -> None:
        """
        Удалить зависимость из словаря зависимостей
        :param name: название зависимости
        """

        if not self.dependencies.get(name):
            raise ValueError("Зависимость не была найдена в словаре зависимостей")

        del self.dependencies[name]

    def create_pyproject(self) -> str:
        final_dependencies = [
            f'{dependency} = "{version}"'
            for dependency, version in self.dependencies.items()
        ]

        return self.pyproject_template + "\n".join(final_dependencies)


def main() -> None:
    """
    Вызвать функции для выполнения логики пост-хука
    """

    create_poetry_dependencies()


def create_poetry_dependencies() -> None:
    """
    Создать файл зависимостей poetry
    """

    creator = DependenciesCreator()
    file_content = creator.create_pyproject()
    file_path = str(Config.template_path / "pyproject.toml")

    with open(file_path, "w") as f:
        f.write(file_content)


if __name__ == '__main__':
    sys.exit(main())