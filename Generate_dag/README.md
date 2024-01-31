# Запуск генерации Dag 
* Перед стартом необходимо запросить файл с токеном для бота


#### Для создания Pipline можно использовать:
* Любую функцию написаную на Python (Более подробно читайте в файле Add_func_DAG.txt)
* Любое соединение в Airbyte (Более подробно читайте в файле Add_func_DAG.txt)
* Запуск Dbt (Как файла start_dbt.py, так и через dbt run Более подробно смотрите в файле Add_func_DAG.txt)


#### Для запуска необходимо изменить файл Config_generate_dag.txt 
* nameDag - Название вашего Dag
* owner - ФИО разработчика 
* schedule_interval - период запуска Dag 
* description - описание Dag
* start_date - Дата с которой будет работать Dag
* retries - Количество попыток запуска при возникновении ошибки 
* retry_delay - Период запуска при ошибке 
* NEXT_LIST_TASK:NEXT_LIST_TASK -Ничего не означает, после этой строки надо начинать записывать Task
* Далее идет список Task's (Как их записывать смотрите в Add_func_DAG.txt)

#### После того как изменили файл Config_generate_dag.txt Можно запускать генерацию DAG 
* dag.py ПУТЬ_к_вашей дирректории Airflow/dags и название нового файла
* ПРИМЕР: Generate_dag.py Airflow/dags/dag_airbyte.py
