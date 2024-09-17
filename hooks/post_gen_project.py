from collections import namedtuple
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
                uvicorn = "^0.30.6"
                pydantic-settings = "^2.5.0"
                dependency-injector = "^4.41.0"
            """
        )

        # словарь зависимостей, где ключ - название библиотеки / фреймворка, значение - версия
        self.dependencies = {
            "strawberry-graphql": "^0.241.0"
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


poetry_creator = DependenciesCreator()


def delete_files(*file_paths: pathlib.Path) -> None:
    """
    Удалить директорию
    :param file_paths: полный путь до директории
    """

    for file_path in file_paths:
        file_path.unlink()


def rename_file(file_path: pathlib.Path, new_name: str) -> None:
    """
    Переименовать файл
    :param file_path: полный путь до директории
    :param new_name: новое название файла
    """

    new_name_file_path = file_path.parent / new_name
    file_path.rename(new_name_file_path)


def main() -> None:
    """
    Вызвать функции для выполнения логики пост-хука
    """

    handle_api_architecture()
    create_poetry_dependencies()


def create_poetry_dependencies() -> None:
    """
    Создать файл зависимостей poetry
    """

    file_content = poetry_creator.create_pyproject()
    file_path = str(Config.template_path / "pyproject.toml")

    with open(file_path, "w") as f:
        f.write(file_content)


def handle_api_architecture() -> None:
    """
    Выбрать реализацию API
    """

    def _choose_rest() -> None:
        """
        Выбрать реализацию REST
        """

        poetry_creator.remove_dependency("strawberry-graphql")

        to_delete = (
            Config.template_path / "web" / "entrypoints" / "graphql_index_entrypoint.py",
            Config.template_path / "web" / "schemas" / "index_schema.py",
            Config.template_path / "web" / "tools" / "graphql_router_registrator.py"
        )

        delete_files(*to_delete)

        RenameFile = namedtuple("RenameFile", ["path", "new_name"])

        to_rename = (
            RenameFile(
                Config.template_path / "web" / "entrypoints" / "rest_index_entrypoint.py",
                "index_entrypoint.py"
            ),
            RenameFile(
                Config.template_path / "web" / "tools" / "rest_router_registrator.py",
                "router_registrator.py"
            )
        )

        for file in to_rename:
            rename_file(file.path, file.new_name)

    def _choose_graphql() -> None:
        """
        Выбрать реализацию GraphQL
        """

        to_delete = (
            Config.template_path / "web" / "entrypoints" / "rest_index_entrypoint.py",
            Config.template_path / "web" / "tools" / "rest_router_registrator.py"
        )

        delete_files(*to_delete)

        RenameFile = namedtuple("RenameFile", ["path", "new_name"])

        to_rename = (
            RenameFile(
                Config.template_path / "web" / "entrypoints" / "graphql_index_entrypoint.py",
                "index_entrypoint.py"
            ),
            RenameFile(
                Config.template_path / "web" / "tools" / "graphql_router_registrator.py",
                "router_registrator.py"
            )
        )

        for file in to_rename:
            rename_file(file.path, file.new_name)

    api_architecture = "{{ cookiecutter.api_architecture }}"
    api_choices = {
        "rest": _choose_rest,
        "graphql": _choose_graphql
    }

    api_choices[api_architecture]()


if __name__ == '__main__':
    sys.exit(main())
