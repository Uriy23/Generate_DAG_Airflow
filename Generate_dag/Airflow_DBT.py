import subprocess
import os
from dwh_yoshi_v1.dbt_transform.start_dbt import load_variables

def read_config_file():
    with open('Config_generate_dag.txt', encoding='utf-8') as file:
        rows = file.readlines()
        default_args = {i.split(':')[0]: i.split(':')[1].replace('\n', '').strip() for i in rows if
                        len(i) > 4}  # Словарь с конфигами
        return default_args

def transport_file():
    src = '.env'
    dst = 'dwh_yoshi_v1/dbt_transform'
    filename = os.path.basename(src)
    dst_file = os.path.join(dst, filename)
    os.rename(src, dst_file)

def start_DBT_file():
    '''Запуск файла start_dbt.py'''
    config = read_config_file()

    #Предусмотреть возможность запуска с аргусментами full/not_full
    script_path = "dwh_yoshi_v1/dbt_transform/start_dbt.py"
    args = [config['dbt_type_start'], "auto"]
    subprocess.call(["python", script_path] + args)


def start_DBT_command():
    '''Запуск dbt используя комнды для командной строки'''
    dbt_command = read_config_file()
    os.chdir('dwh_yoshi_v1/dbt_transform')
    subprocess.run(dbt_command['dbt_type_start'], shell=True, check=True)


def start_DBT_TASK():
    '''Главная Функция запуска Dbt'''
    config = read_config_file()

    cmd_git_clone = f'git clone https://{config["LOGIN_bitbucket"]}@bitbucket.org/s25-ds/dwh_yoshi_v1.git'
    try:
        subprocess.call(cmd_git_clone)
        transport_file()
        subprocess.run('pip install dbt-postgres', shell=True, check=True)
        load_variables()
        subprocess.run('dbt deps', shell=True)
    except BaseException:#В случае если репозиторий уже склонирован и .env перенесен
        pass

    if (config['dbt_type_start'] != 'full') and (config['dbt_type_start']!='not_full'):
        start_DBT_command()
    else:
        start_DBT_file()


start_DBT_TASK()
