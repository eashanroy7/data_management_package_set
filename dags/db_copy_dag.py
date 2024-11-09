from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from your_script import copy_data_to_clean_db, copy_clean_to_env, load_db_config

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('db_copy_dag', default_args=default_args, schedule_interval='@daily') as dag:

    # Load database configuration
    db_config = load_db_config()

    # Task to copy data from Production to Clean DB
    copy_to_clean_task = PythonOperator(
        task_id='copy_to_clean',
        python_callable=copy_data_to_clean_db,
        op_kwargs={'prod_db_conn_str': 'your_prod_conn', 'clean_db_conn_str': 'your_clean_conn'}
    )

    # Task to copy data from Clean DB to each environment based on config
    for db in db_config:
        copy_task = PythonOperator(
            task_id=f'copy_to_{db["name"]}',
            python_callable=copy_clean_to_env,
            op_kwargs={
                'clean_db_conn_str': 'your_clean_conn',
                'env_db_conn_str': f'your_{db["name"].lower()}_conn',
                'batch_size': db['batch_size'],
                'filter_criteria': db['filter_criteria']
            }
        )

    copy_to_clean_task >> [copy_task]
