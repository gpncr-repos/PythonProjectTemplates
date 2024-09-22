from collections import namedtuple
import dataclasses
import pathlib
import shutil
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
            "strawberry-graphql": "^0.241.0",
            "grpcio": "^1.66.1",
            "grpcio-tools": "^1.66.1"
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


def remove_files(*files_paths: pathlib.Path) -> None:
    """
    Удалить файлы
    :param files_paths: полный путь до файлов
    """

    for file_path in files_paths:
        file_path.unlink()


def remove_directories(*directories_paths: pathlib.Path) -> None:
    """
    Удалить директории
    :param directories_paths: полный путь до директорий
    """

    for directory_path in directories_paths:
        shutil.rmtree(directory_path)


def rename_file(file_path: pathlib.Path, new_name: str) -> None:
    """
    Переименовать файл
    :param file_path: полный путь до директории
    :param new_name: новое название файла
    """

    new_name_file_path = file_path.parent / new_name
    file_path.rename(new_name_file_path)


RenameFile = namedtuple("RenameFile", ["path", "new_name"])


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

        files_to_delete = (
            Config.template_path / "web" / "entrypoints" / "graphql_index_entrypoint.py",
            Config.template_path / "web" / "entrypoints" / "grpc_index_entrypoint.py",
            Config.template_path / "web" / "schemas" / "index_schema.py",
            Config.template_path / "web" / "tools" / "grpc_channels.py",
            Config.template_path / "web" / "tools" / "grpc_server.py",
            Config.template_path / "web" / "tools" / "service_registrator.py",
            Config.template_path / "services" / "index_service.py",
            Config.template_path / "interfaces" / "base_grpc_channel.py"
        )

        remove_files(*files_to_delete)

        directories_to_delete = (
            Config.template_path / "protobufs",
        )

        remove_directories(*directories_to_delete)

        to_rename = (
            RenameFile(
                Config.template_path / "web" / "entrypoints" / "rest_index_entrypoint.py",
                "index_entrypoint.py"
            ),
        )

        for file in to_rename:
            rename_file(file.path, file.new_name)

    def _choose_graphql() -> None:
        """
        Выбрать реализацию GraphQL
        """

        files_to_delete = (
            Config.template_path / "web" / "entrypoints" / "rest_index_entrypoint.py",
            Config.template_path / "web" / "entrypoints" / "grpc_index_entrypoint.py",
            Config.template_path / "web" / "tools" / "grpc_channels.py",
            Config.template_path / "web" / "tools" / "grpc_server.py",
            Config.template_path / "web" / "tools" / "service_registrator.py",
            Config.template_path / "services" / "index_service.py",
            Config.template_path / "interfaces" / "base_grpc_channel.py"
        )

        remove_files(*files_to_delete)

        directories_to_delete = (
            Config.template_path / "protobufs",
        )

        remove_directories(*directories_to_delete)

        to_rename = (
            RenameFile(
                Config.template_path / "web" / "entrypoints" / "graphql_index_entrypoint.py",
                "index_entrypoint.py"
            ),
        )

        for file in to_rename:
            rename_file(file.path, file.new_name)

    def _choose_grpc() -> None:
        """
        Выбрать реализацию GraphQL
        """

        files_to_delete = (
            Config.template_path / "web" / "entrypoints" / "rest_index_entrypoint.py",
            Config.template_path / "web" / "entrypoints" / "graphql_index_entrypoint.py",
            Config.template_path / "web" / "schemas" / "index_schema.py"
        )

        remove_files(*files_to_delete)

        to_rename = (
            RenameFile(
                Config.template_path / "web" / "entrypoints" / "grpc_index_entrypoint.py",
                "index_entrypoint.py"
            ),
        )

        for file in to_rename:
            rename_file(file.path, file.new_name)

    api_architecture = "{{ cookiecutter.api_architecture }}"
    api_choices = {
        "rest": _choose_rest,
        "graphql": _choose_graphql,
        "grpc": _choose_grpc
    }

    api_choices[api_architecture]()


if __name__ == '__main__':
    sys.exit(main())
