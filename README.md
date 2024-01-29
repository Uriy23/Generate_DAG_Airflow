# Интеграция Airbyte с Airflow 

#### Для запуска необходимо изменить файл for_dag.txt 
* nameDag - Название вашего Dag
* owner - ФИО разработчика 
* schedule_interval - период запуска Dag 
* description - описание Dag
* start_date - Дата с которой будет работать Dag
* retries - Количество попыток запуска при возникновении ошибки 
* retry_delay - Период запуска при ошибке 
* airbyte_conn_id - Уникальное имя соединения (Подробнее в файле Connect_Airflow_Airbyte)
* name_con_1 - ИД Connection Airbyte находится в URl после /connections/

Название Connection в файле for_dag.txt должно начинаться с name_ и далее
любое название 