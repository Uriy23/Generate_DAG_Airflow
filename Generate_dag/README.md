# Интеграция Airbyte с Airflow 
* Перед стартом необходимо запросить файл с токеном для бота

#### Для запуска необходимо изменить файл for_dag.txt 
* nameDag - Название вашего Dag
* owner - ФИО разработчика 
* schedule_interval - период запуска Dag 
* description - описание Dag
* start_date - Дата с которой будет работать Dag
* retries - Количество попыток запуска при возникновении ошибки 
* retry_delay - Период запуска при ошибке 
* airbyte_conn_id - Уникальное имя соединения (Подробнее в файле Connect_Airflow_Airbyte)
* name_PP_ - ИД для Postgres-Postgres Connection Airbyte находится в URl после /connections/
* name_PCH - ИД для соедениний Postgres-CH

Название Connection в файле for_dag.txt должно начинаться с name_ и далее
любое название 

#### После того как изменили файл for_dag.txt Можно запускать генерацию DAG 
* dag.py ПУТЬ_к_вашей дирректории Airflow/dags и название нового файла
* ПРИМЕР: dag.py Airflow/dags/dag_airbyte.py
