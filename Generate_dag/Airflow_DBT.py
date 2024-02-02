import subprocess
import os


def before_launch_DBT():
    os.chdir('dwh_yoshi_v1/dbt_transform')
    from dwh_yoshi_v1.dbt_transform.start_dbt import load_variables
    load_variables()
    print('переменныее загружены')

    subprocess.run('dbt deps', shell=True)
    subprocess.run("python ../src/get_currency.py", shell=True, check=True)
    subprocess.run('dbt seed', shell=True)


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
    print('Файл перенесен')

def start_DBT_file(config):
    '''Запуск файла start_dbt.py'''

    os.chdir('dwh_yoshi_v1/dbt_transform')
    script_path = "start_dbt.py"
    args = [config['dbt_type_start'], "auto"]
    subprocess.call(["python", script_path] + args)


def start_DBT_command(config):
    '''Запуск dbt используя комнды для командной строки'''

    dbt_command = config
    before_launch_DBT()
    subprocess.run(dbt_command['dbt_type_start'], shell=True, check=True)


def start_DBT_TASK():
    '''Главная Функция запуска Dbt'''
    config = read_config_file()
    list_lib = ['dbt-postgres','pandas','numpy','yfinance']

    cmd_git_clone = f'git clone https://{config["dbt_LOGIN_bitbucket"]}@bitbucket.org/s25-ds/dwh_yoshi_v1.git'
    try:
        subprocess.call(cmd_git_clone)
        transport_file()
        subprocess.run(f'pip install {" ".join(list_lib)}', shell=True, check=True)
    except Exception as expc:#В случае если репозиторий уже склонирован и .env перенесен
        print(expc)


    if (config['dbt_type_start'] != 'full') and (config['dbt_type_start']!='not_full'):
        start_DBT_command(config)
    else:
        start_DBT_file(config)

# start_DBT_TASK()
