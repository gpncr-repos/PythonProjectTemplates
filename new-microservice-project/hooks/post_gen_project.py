import os
import shutil

import yaml

BASE_DIR = os.getcwd()


def merge_docker_compose(files):
    merged = {'version': None, 'services': {}, 'networks': {}, 'volumes': {}}

    for file in files:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)

            # Объединяем версии
            if merged['version'] is None:
                merged['version'] = data.get('version')
            elif merged['version'] != data.get('version'):
                print(f"Warning: Versions do not match in {file}")

            # Объединяем сервисы
            if 'services' in data:
                merged['services'].update(data['services'])

            # Объединяем сети
            if 'networks' in data:
                merged['networks'].update(data['networks'])

            # Объединяем тома
            if 'volumes' in data:
                merged['volumes'].update(data['volumes'])
    merged = {key: val for key, val in merged.items() if val}
    return merged


def represent_none(self, _):
    # Заменяет null на пустую строку при dump'е
    return self.represent_scalar('tag:yaml.org,2002:null', '')


def save_merged_file(merged_data, output_file):
    yaml.add_representer(type(None), represent_none)
    with open(output_file, 'w') as f:
        yaml.dump(merged_data, f, sort_keys=False)


def remove_files(path_to_remove):
    if os.path.isfile(path_to_remove):
        os.remove(path_to_remove)
        print(f'File with path {path_to_remove} was removed')
    elif os.path.isdir(path_to_remove):
        shutil.rmtree(path_to_remove)
        print(f'Directory with path {path_to_remove} was removed')


def clear_settings(*module_names):
    settings_path = os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/config/settings.py')
    with open(settings_path, "r") as file:
        lines = file.readlines()
    filtered_lines = []
    for line in lines:
        write = True
        for module in module_names:
            if module in line:
                write = False
                break
        if write:
            filtered_lines.append(line)
    with open(settings_path, 'w') as file:
        for line in filtered_lines:
            file.write(line)


add_postgres = '{{cookiecutter.add_postgres}}' == 'True'
add_redis = '{{cookiecutter.add_redis}}' == 'True'
add_kafka = '{{cookiecutter.add_kafka}}' == 'True'

to_compose = [os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/to_compose/app.yaml')]
to_remove = []
to_clear_from_settings = []

if not add_postgres:
    pg_paths = [
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/config/postgres_settings.py'),
    ]
    to_remove.extend(pg_paths)
    to_clear_from_settings.append("postgres")
else:
    to_compose.append(
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/to_compose/postgres.yaml'))

if not add_redis:
    redis_paths = [
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}',
                     'src/tools/factories/redis_connection_factory.py'),
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/config/redis_settings.py'),
    ]
    to_remove.extend(redis_paths)
    to_clear_from_settings.append("redis")
else:
    to_compose.append(os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/to_compose/redis.yaml'))

if not add_kafka:
    kafka_paths = [
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/brokers/kafka.py'),
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/interfaces/message_broker.py'),
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/config/kafka_settings.py'),
    ]
    to_remove.extend(kafka_paths)
    to_clear_from_settings.append("kafka")
else:
    to_compose.append(os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/to_compose/kafka.yaml'))

merged_data = merge_docker_compose(to_compose)
compose_file_path = os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/docker-compose.yaml')
save_merged_file(merged_data, compose_file_path)

to_remove.append(os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/to_compose'))
for path in to_remove:
    remove_files(path)

clear_settings(*to_clear_from_settings)
