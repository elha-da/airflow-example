import datetime, logging
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    "depends_on_past": False,
    'email': ['email@example.io'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=10)
}

second_var = Variable.get(key="my_second_var", default_var='default_var')
Variable.set(key="my_first_var", value='first_var_value')


def init_vars(ds, **kwargs):
    logging.info(f"time : {ds}")
    logging.info(datetime.datetime.strptime(ds, '%Y-%m-%d'))
    first_var = Variable.get(key="my_first_var", default_var='default_var')
    logging.info(first_var)
    return first_var


with DAG(
    'example_dag', 
    start_date=datetime.datetime(2021, 3, 26),
    schedule_interval='@hourly',
    default_args=default_args,
    description="Dummy Dag example"
) as dag:
    oper = DummyOperator(task_id='op')

    run_this = PythonOperator(
        task_id="run_this", 
        python_callable=init_vars, 
        provide_context=True
    )

    bash_task = BashOperator(
        task_id="bash_task",
        bash_command=f'echo "Here is the message: { second_var } "',
        dag=dag
    )

oper
run_this >> bash_task
