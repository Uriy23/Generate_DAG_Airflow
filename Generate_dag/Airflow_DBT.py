import subprocess
import os

def transport_file():
    src = '.env'
    dst = 'dwh_yoshi_v1/dbt_transform'
    filename = os.path.basename(src)
    dst_file = os.path.join(dst, filename)
    os.rename(src, dst_file)

def start_DBT_file(type_):
    '''Запуск файла start_dbt.py'''
    if type_ == None:
        type_ = 'not_full'
    #Предусмотреть возможность запуска с аргусментами full/not_full
    script_path = "dwh_yoshi_v1/dbt_transform/start_dbt.py"
    args = [type_, "auto"]
    subprocess.call(["python", script_path] + args)

def read_config_file():
    with open('Config_generate_dag.txt') as file:
        rows = file.readlines()
        default_args = {i.split(':')[0]: i.split(':')[1].replace('\n', '').strip() for i in rows if
                        len(i) > 4}  # Словарь с конфигами
        return default_args

def start_DBT_command():
    '''Запуск dbt используя комнды для командной строки'''
    dbt_command = read_config_file['dbt_command']
    subprocess.call(dbt_command)


def start_DBT_TASK(type_start):
    '''Главная Функция запуска Dbt'''
    cmd_git_clone = 'git clone https://Chupakhin_uriy@bitbucket.org/s25-ds/dwh_yoshi_v1.git'
    subprocess.call(cmd_git_clone)
    transport_file()
    if (type_start != 'full') and (type_start!='not_full'):
        start_DBT_command()
    else:
        start_DBT_file(type_start)


