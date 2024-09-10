import pathlib
import shutil
import sys

# Костыль, связанный с особенностью работы cookiecutter - он будет видеть только те локальные модули, которые
# находятся в директории с шаблоном
project_directory = pathlib.Path.cwd().resolve()
sys.path.insert(0, str(project_directory))

from cookiecutter_utils import config, dependencies

template_config = config.template_config

def main() -> None:
    """
    Вызвать функции для выполнения логики пост-хука
    """

    create_poetry_dependencies()
    remove_cookiecutter_utils()


def create_poetry_dependencies() -> None:
    """
    Создать файл зависимостей poetry
    """

    creator = dependencies.DependenciesCreator()
    file_content = creator.create_pyproject()
    file_path = str(template_config.template_src_path / "pyproject.toml")

    with open(file_path, "w") as f:
        f.write(file_content)


def remove_cookiecutter_utils() -> None:
    """
    Удалить утилиты для работы cookiecutter
    """

    directory_to_drop = project_directory / "cookiecutter_utils"
    shutil.rmtree(str(directory_to_drop))


if __name__ == '__main__':
    sys.exit(main())
