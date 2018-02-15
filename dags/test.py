from airflow import DAG
from datetime import datetime, timedelta
from plugins.ssh_postgres_plugin.operators.ssh_postgres_operator import SSHPostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'start_date': datetime(2018, 1, 1, 0, 0),
    'email': ['l5t3o4a9m9q9v1w9@astronomerteam.slack.com'],
    'email_on_failure': True,
    'email_on_retry': False
}

dag = DAG(
    'a_test_ssh_tunnel',
    schedule_interval='@once',
    default_args=default_args,
    catchup=False
)

kick_off_dag = DummyOperator(
    task_id='kick_off_dag',
    dag=dag
)

sql = """
SELECT * FROM bamboo_hr.employee_directory
"""
with dag:
    test = SSHPostgresOperator(task_id='check_for_tunnel',
                               postgres_conn_id='rtr_redshift',
                               sql=sql,
                               create_tunnel=True)

    kick_off_dag >> test
