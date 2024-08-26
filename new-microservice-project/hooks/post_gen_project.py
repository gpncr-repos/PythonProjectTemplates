import os
import shutil

BASE_DIR = os.getcwd()


def remove(path_to_remove):
    if os.path.isfile(path_to_remove):
        os.remove(path_to_remove)
        print(f'File with path {path_to_remove} was removed')
    elif os.path.isdir(path_to_remove):
        shutil.rmtree(path_to_remove)
        print(f'Directory with path {path_to_remove} was removed')


add_postgres = '{{cookiecutter.add_postgres}}' == 'True'
add_redis = '{{cookiecutter.add_redis}}' == 'True'
add_kafka = '{{cookiecutter.add_kafka}}' == 'True'


if not add_postgres:
    paths = [
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/config/db_settings.py'),
    ]
    for path in paths:
        remove(path)


if not add_redis:
    paths = [
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/tools/factories/redis_connection.py'),
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/config/redis_settings.py'),
    ]
    for path in paths:
        remove(path)

if not add_kafka:
    paths = [
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/brokers/kafka.py'),
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/interfaces/message_broker.py'),
        os.path.join(BASE_DIR, 'backend', '{{cookiecutter.service_name}}', 'src/config/kafka_settings.py'),
    ]
    for path in paths:
        remove(path)
