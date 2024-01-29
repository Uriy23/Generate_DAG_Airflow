
def start_text_dag_func(owner,schedule_interval, start_date, retries,retry_delay,description,nameDag):
    text_start = f'''
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator


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
    schedule_interval="{schedule_interval}"
)
'''
    return text_start
def text_func(name_con,con_id,airbyte_conn_id):
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
    return '\n'+('>>').join(list_).strip()

def read_conf():
    with open('for_dag.txt', encoding='utf-8') as file:
        rows = file.readlines()
    return rows

def create_python_file():

    rows = read_conf()
    list_name_conn = []
    # airflow / dags /
    with open('dag_airbyte.py','w',encoding='utf-8') as file_dag:

        default_args = {i.split(':')[0]:i.split(':')[1].replace('\n','').strip() for i in rows if len(i)>4}

        start_text_dag = start_text_dag_func(
                       owner=default_args['owner'],
                       start_date=default_args['start_date'],
                       retries=default_args['retries'],
                       schedule_interval = default_args['schedule_interval'],
                       retry_delay=default_args['retry_delay'],
                       description=default_args['description'],
                       nameDag=default_args['nameDag']
        )
        file_dag.write(start_text_dag)


        for row in default_args:
            if 'name_' in row:
                list_name_conn.append(f'start_airbyte{row}')
                con_id = default_args[row]
                text_func_connection = text_func(name_con=row,
                                                 con_id=con_id,
                                                 airbyte_conn_id=default_args['airbyte_conn_id'])
                file_dag.write(text_func_connection)
        file_dag.write(create_end_dags(list_name_conn).replace('  ',''))



create_python_file()