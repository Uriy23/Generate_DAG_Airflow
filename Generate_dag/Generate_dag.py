import sys

def get_tokens_tg():
    with open('Api_tg.txt', encoding='utf-8') as file:
        rows = file.readlines()
        API_tg = {i.split(':')[0]: i.split(':')[1].replace('\n', '').strip() for i in rows if len(i)>3}
    return API_tg

def create_allert_on_tg(tokens):

    text_allert = f'''
def on_failure_callback(context):    
    message = "Task failed. DAG: {{0}}, Task: {{1}}, Execution date: {{2}}".format(
        context['task_instance'].dag_id, 
        context['task_instance'].task_id,
        context['execution_date'])
    for chat_id_person in {tokens['chat_id'].split(' ')}:
        telegram_op = TelegramOperator(task_id='send_telegram',
                                   token="{tokens['token'].replace('|',':')}", 
                                   chat_id=chat_id_person,
                                   text=message)
        telegram_op.execute(context=context)'''
    return text_allert



def start_text_dag_func(owner, schedule_interval, start_date, retries, retry_delay, description, nameDag):
    '''Создаем начало файла и заполняем конфиги'''
    global create_allert_on_tg,get_tokens_tg
    text_start = f'''
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator

{create_allert_on_tg(get_tokens_tg())}

default_args = {{
    'owner': "{owner}",
    'depends_on_past': False,
    'start_date': {start_date},
    'retries': {retries},
    'retry_delay': {retry_delay},
}}

dag = DAG(
    "{nameDag}",
    default_args=default_args,
    description="{description}",
    schedule_interval="{schedule_interval}",
    on_failure_callback=on_failure_callback
)
'''
    return text_start


def Airbyte_PP(name_con, con_id, airbyte_conn_id):
    """Шаблон для Создания оператора для каждого Connections из Airbyte Postgres-Postgres"""
    text_func = f'''
start_airbyte{name_con} = AirbyteTriggerSyncOperator(
         task_id = "{name_con}",
         airbyte_conn_id = "{airbyte_conn_id}",
         connection_id ="{con_id}",
         asynchronous=False,
         timeout=3600,
         wait_seconds =3,
         dag=dag
     )
    '''
    return text_func


def create_end_dags(list_):
    """Создаем последовательность запуска всех COnnerctions Airbyte"""
    return '\n' + '>>'.join(list_).strip()


def read_conf():
    """Читаем конфиги"""
    with open('Config_generate_dag.txt', encoding='utf-8') as file:
        rows = file.readlines()
    return rows


def DBT_start_code():
    # 1. git clone
#     2. Запуск файла start_dbt.py
    pass
def Airbyte_PCH():
    """Шаблон для Создания оператора для каждого Connections из Airbyte Postgres-CH"""
    pass


def create_python_file(path_folder_airflow):
    """Основная функция
    Создаем и заполняем файл .py
    """

    rows = read_conf()
    list_name_conn = []  # Переменная для использования последовательного запуска операторов

    with open(f'{path_folder_airflow}', 'w', encoding='utf-8') as file_dag:

        default_args = {i.split(':')[0]: i.split(':')[1].replace('\n', '').strip() for i in rows if
                        len(i) > 4}  # Словарь с конфигами

        start_text_dag = start_text_dag_func(
            owner=default_args['owner'],
            start_date=default_args['start_date'],
            retries=default_args['retries'],
            schedule_interval=default_args['schedule_interval'],
            retry_delay=default_args['retry_delay'],
            description=default_args['description'],
            nameDag=default_args['nameDag']
        )
        file_dag.write(start_text_dag)
#Ищем только ID Connections Airbyte для создания операторов
        for row in default_args:
            if 'name_' in row:
                list_name_conn.append(f'start_airbyte{row}')
                con_id = default_args[row]
                text_func_connection = Airbyte_code(name_con=row,
                                                 con_id=con_id,
                                                 airbyte_conn_id=default_args['airbyte_conn_id'])
                file_dag.write(text_func_connection)
        file_dag.write(create_end_dags(list_name_conn).replace('  ', ''))

#При запуске передаем путь и название новго файла (Файл должен быть сохранен в Airflow/dags/)
if __name__ == "__main__":
    folder_airflow = str(sys.argv[1])
    create_python_file(path_folder_airflow=folder_airflow)