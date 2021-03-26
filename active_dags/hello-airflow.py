import logging
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils import dates

logging.basicConfig(format="%(name)s-%(levelname)s-%(asctime)s-%(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

default_args = {
    "owner": "admin airflow",
    "description": (
        "DAG to explain airflow concepts"
    ),
    "depends_on_past": False,
    "start_date": dates.days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "provide_context": True,
}


def task_1(**kwargs):
    logger.info('=====Executing Task 1=============')
    return kwargs['message']


def task_2(**kwargs):
    logger.info('=====Executing Task 2=============')
    task_instance = kwargs['ti']
    result = task_instance.xcom_pull(key=None, task_ids='Task_1')
    logger.info('Extracted the value from task 1')
    logger.info(result)


with DAG(
    "hello_airflow",
    default_args=default_args,
    schedule_interval=timedelta(minutes=60),
) as new_dag:

    task1 = PythonOperator(
        task_id='Task_1',
        python_callable=task_1,
        op_kwargs={'message': 'hello airflow'},
        provide_context=True
    )

    task2 = PythonOperator(
        task_id='Task_2',
        python_callable=task_2,
        op_kwargs=None,
        provide_context=True
    )

task1 >> task2
