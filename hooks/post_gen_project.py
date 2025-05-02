import dataclasses
import os
import pathlib
import shutil
import sys
import textwrap

import yaml


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
                pre-commit = "^4.0.1"
                python-json-logger = "^2.0.7"
                pytest = "^8.3.5"
                pytest-asyncio = "^0.26.0"
            """
        )

        # словарь зависимостей, где ключ - название библиотеки / фреймворка, значение - версия
        self.dependencies = {}

    def remove_dependency(self, name: str) -> None:
        """
        Удалить зависимость из словаря зависимостей
        :param name: название зависимости
        """

        if not self.dependencies.get(name):
            raise ValueError("Зависимость не была найдена в словаре зависимостей")

        del self.dependencies[name]

    def add_dependency(self, dep: dict[str, str]) -> None:
        """
        Добавить зависимость в словарь зависимостей
        :param dep: словарь с именем и версией зависимости
        """

        self.dependencies.update(dep)

    def create_pyproject(self) -> str:
        final_dependencies = [
            f'{dependency} = "{version}"' for dependency, version in self.dependencies.items()
        ]

        return self.pyproject_template + "\n".join(final_dependencies)


class FileManager:
    def __init__(self):
        self.paths_to_remove: list[pathlib.Path | None] = []

    def remove_files(self) -> None:
        """
        Удалить файл или директорию
        """

        for path in self.paths_to_remove:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    def rename_file(self, file_path: pathlib.Path, new_name: str) -> None:
        """
        Переименовать файл
        :param file_path: полный путь до директории
        :param new_name: новое название файла
        """

        new_name_file_path = file_path.parent / new_name
        file_path.rename(new_name_file_path)


class DockerComposeMerger:
    def __init__(self):
        self.files_to_compose = set()

    def _merge_docker_compose(self) -> dict:
        """
        Собрать словарь из yaml файлов
        :return: собранный словарь
        """

        merged = {"version": None, "services": {}, "networks": {}, "volumes": {}}

        for file in self.files_to_compose:
            with open(file, "r") as f:
                data = yaml.safe_load(f)

                if merged["version"] is None:
                    merged["version"] = data.get("version")
                elif merged["version"] != data.get("version"):
                    print(f"Warning: Versions do not match in {file}")

                if "services" in data:
                    merged["services"].update(data["services"])

                if "networks" in data:
                    merged["networks"].update(data["networks"])

                if "volumes" in data:
                    merged["volumes"].update(data["volumes"])
        merged = {key: val for key, val in merged.items() if val}
        return merged

    def save_merged_file(self, output_file_path: pathlib.Path) -> None:
        """
        Сохранить собранный yaml-файл
        :param output_file_path: путь для сохранения
        """

        def _represent_none(self, _):
            # Заменяет null на пустую строку при dump'е
            return self.represent_scalar("tag:yaml.org,2002:null", "")

        yaml.add_representer(type(None), _represent_none)
        merged_data = self._merge_docker_compose()
        with open(output_file_path, "w") as f:
            yaml.dump(merged_data, f, sort_keys=False)


class LibsConfig:
    """
    Содержит поля с именем в виде названия библиотеки,
    и значением в виде словаря с путями до зависимых модулей и
    docker-compose файла, а также необходимыми зависимостями
    """

    sqlalchemy = {
        "modules": [
            Config.template_path / "config" / "pg_config.py",
            Config.template_path / "interfaces" / "base_alchemy_model.py",
            Config.template_path / "repositories" / "base_alchemy_repository.py",
            Config.template_path / "storage" / "sqlalchemy",
            Config.template_path / "tools" / "di_containers" / "alchemy_container.py",
            Config.template_path / "tools" / "factories" / "alchemy_engine_factory.py",
            Config.template_path / "uows" / "alchemy_uow.py",
            Config.template_path.parent / "docs" / "postgres-sqlalchemy.md",
        ],
        "compose": Config.template_path / "to_compose" / "postgres.yaml",
        "dependencies": {
            "sqlalchemy": "^2.0.0",
            "alembic": "^1.13.0",
            "asyncpg": "^0.29.0",
            "psycopg2": "^2.9.0",
        },
    }
    raw_postgres = {
        "modules": [
            Config.template_path / "config" / "pg_config.py",
            Config.template_path / "interfaces" / "base_postgres_cursor_proxy.py",
            Config.template_path / "storage" / "raw_postgres",
            Config.template_path / "repositories" / "asyncpg_repository.py",
            Config.template_path / "repositories" / "psycopg_repository.py",
            Config.template_path / "uows" / "asyncpg_uow.py",
            Config.template_path / "uows" / "psycopg_uow.py",
            Config.template_path / "tools" / "di_containers" / "raw_postgres_container.py",
            Config.template_path / "tools" / "factories" / "asyncpg_connection_pool_factory.py",
            Config.template_path / "tools" / "factories" / "psycopg_connection_pool_factory.py",
            Config.template_path.parent / "docs" / "raw-postgres.md",
            Config.template_path.parent / "docs" / "raw-asyncpg-uml.png",
        ],
        "compose": Config.template_path / "to_compose" / "postgres.yaml",
        "dependencies": {
            "asyncpg": "^0.29.0",
            "psycopg": "^3.2.0",
            "psycopg-pool": "^3.2.0",
            "psycopg-binary": "^3.2.3"
        },
    }
    redis = {
        "modules": [
            Config.template_path / "config" / "redis_config.py",
            Config.template_path / "repositories" / "redis_repository.py",
            Config.template_path / "tools" / "di_containers" / "redis_container.py",
            Config.template_path / "storage" / "redis",
            Config.template_path.parent / "docs" / "redis-cache.md",
            Config.template_path / "uows" / "redis_uow.py",
        ],
        "compose": Config.template_path / "to_compose" / "redis.yaml",
        "dependencies": {
            "redis": "^5.0.0",
        },
    }
    kafka = {
        "modules": [
            Config.template_path / "brokers",
            Config.template_path / "brokers" / "kafka",
            Config.template_path / "config" / "kafka_config.py",
            Config.template_path / "interfaces" / "base_message_broker.py",
            Config.template_path / "models" / "dto" /"broker_message_dto.py",
            Config.template_path / "tools" / "di_containers" / "kafka_di_container.py",
            Config.template_path.parent / "docs" / "kafka.md",
        ],
        "compose": Config.template_path / "to_compose" / "kafka.yaml",
        "dependencies": {"aiokafka": "^0.11.0"},
    }
    rabbitmq = {
        "modules": [
            Config.template_path / "brokers",
            Config.template_path / "brokers" / "rabbitmq",
            Config.template_path / "config" / "rabbitmq_config.py",
            Config.template_path / "interfaces" / "base_rabbitmq_routing_configurator.py",
            Config.template_path / "interfaces" / "base_message_broker.py",
            Config.template_path / "models" / "dto" / "broker_message_dto.py",
            Config.template_path / "tools" / "di_containers" / "rabbitmq_di_container.py",
            Config.template_path.parent / "docs" / "rabbitmq.md",
        ],
        "compose": Config.template_path / "to_compose" / "rabbitmq.yaml",
        "dependencies": {"aio-pika": "^9.4.3"},
    }
    httpx = {
        "modules": [
            Config.template_path / "models" / "dto" / "http_dto.py",
            Config.template_path / "repositories" / "http_connection_proxy.py",
            Config.template_path / "repositories" / "http_repository.py",
            Config.template_path / "tools" / "di_containers" / "http_integration_di_container.py",
            Config.template_path / "uows" / "http_uow.py",
            Config.template_path.parent / "docs" / "httpx.md",
        ],
        "dependencies": {"httpx": "^0.27.2"},
    }
    # TODO: Дополнять в процессе добавления библиотек


poetry_creator = DependenciesCreator()
file_manager = FileManager()
compose_merger = DockerComposeMerger()


def create_poetry_dependencies() -> None:
    """
    Создать файл зависимостей poetry
    """

    file_content = poetry_creator.create_pyproject()
    file_path = str(Config.template_path / "pyproject.toml")

    with open(file_path, "w") as f:
        f.write(file_content)


def resolve_libs() -> None:
    """
    Собрать Docker-Compose и удалить лишние модули
    """

    libs_to_add = {
        "sqlalchemy": "{{cookiecutter.add_sql_alchemy}}" == "True",
        "raw_postgres": "{{cookiecutter.add_raw_postgres}}" == "True",
        "redis": "{{cookiecutter.add_redis}}" == "True",
        "kafka": "{{cookiecutter.add_kafka}}" == "True",
        "rabbitmq": "{{cookiecutter.add_rabbitmq}}" == "True",
        "httpx": "{{cookiecutter.add_httpx}}" == "True",
        # TODO: Дополнять в процессе добавления библиотек
    }

    modules_to_reserve = set()
    modules_to_delete = set()

    for lib in libs_to_add:
        if not libs_to_add[lib]:
            for module in getattr(LibsConfig, lib)["modules"]:
                modules_to_delete.add(module)
        else:
            for module in getattr(LibsConfig, lib)["modules"]:
                modules_to_reserve.add(module)

            compose_path = getattr(LibsConfig, lib).get("compose")
            if compose_path:
                compose_merger.files_to_compose.add(compose_path)
            dependencies = getattr(LibsConfig, lib)["dependencies"]
            poetry_creator.add_dependency(dependencies)

    compose_merger.files_to_compose.add(Config.template_path / "to_compose" / "app.yaml")
    compose_merger.save_merged_file(Config.template_path / "docker-compose.yaml")

    file_manager.paths_to_remove.append(Config.template_path / "to_compose")

    for module in modules_to_delete - modules_to_reserve:
        file_manager.paths_to_remove.append(module)


def rename_env_example():
    file_manager.rename_file(Config.template_path / ".env.example", ".env")


def main() -> None:
    """
    Вызвать функции для выполнения логики пост-хука
    """

    resolve_libs()
    create_poetry_dependencies()
    file_manager.remove_files()
    rename_env_example()


if __name__ == "__main__":
    sys.exit(main())
