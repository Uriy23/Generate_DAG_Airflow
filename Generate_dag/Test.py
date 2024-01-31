
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.operators.python_operator import PythonOperator
from Airflow_DBT import start_DBT_TASK
from Airflow_python_func import *


def on_failure_callback(context):    
    message = "Task failed. DAG: {0}, Task: {1}, Execution date: {2}".format(
        context['task_instance'].dag_id, 
        context['task_instance'].task_id,
        context['execution_date'])
    for chat_id_person in ['731928058', '149461095']:
        telegram_op = TelegramOperator(task_id='send_telegram',
                                   token="6977007865:AAFT10W2LACQk_2DVURFcrwCShB_TT20Cc8", 
                                   chat_id=chat_id_person,
                                   text=message)
        telegram_op.execute(context=context)

default_args = {
    'owner': "Chupakhin Yuriy",
    'depends_on_past': False,
    'start_date': datetime(2024,1,26),
    'retries': 3,
    'retry_delay': timedelta(minutes=30),
}

dag = DAG(
    "Airbate",
    default_args=default_args,
    description="Описание дага",
    schedule_interval="0 2 * * *",
    on_failure_callback=on_failure_callback
)

start_airbytename_airbyte_Postgres_Postgres = AirbyteTriggerSyncOperator(
         task_id = "name_airbyte_Postgres_Postgres",
         airbyte_conn_id = "airbyte",
         connection_id ="7bfc7c83-60d6-443b-aa36-5014916afdfe",
         asynchronous=False,
         timeout=3600,
         wait_seconds =3,
         dag=dag
     )
    
start_airbytename_airbyte_con_2 = AirbyteTriggerSyncOperator(
         task_id = "name_airbyte_con_2",
         airbyte_conn_id = "airbyte",
         connection_id ="16e7fe82a-f3e8-4c6e-9899-9c0f84d72099",
         asynchronous=False,
         timeout=3600,
         wait_seconds =3,
         dag=dag
     )
    
python_func_download_file = PythonOperator(
    task_id='python_func_download_file',
    python_callable=download_file,
    dag=dag
    )
run_DBT = PythonOperator(
    task_id='run DBT',
    python_callable=start_DBT_TASK,
    dag=dag
    )
start_airbytename_airbyte_con_3 = AirbyteTriggerSyncOperator(
         task_id = "name_airbyte_con_3",
         airbyte_conn_id = "airbyte",
         connection_id ="16e7fe82a-f3e8-4c6e-9899-9c0f84d72099",
         asynchronous=False,
         timeout=3600,
         wait_seconds =3,
         dag=dag
     )
    
python_func_save_file = PythonOperator(
    task_id='python_func_save_file',
    python_callable=save_file,
    dag=dag
    )
start_airbytename_airbyte_Postgres_Postgres>>start_airbytename_airbyte_con_2>>python_func_download_file>>run_DBT>>start_airbytename_airbyte_con_3>>python_func_save_file