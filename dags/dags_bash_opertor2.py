'''
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import datetime
import pendulum
'''

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
import pendulum

def random_branch_path():
    from random import randint

    return "cal_a_id" if randint(1, 2) == 1 else "cal_m_id"

def calc_add(x, y, **kwargs):
    result = x + y
    print("x + y : ", result)
    kwargs['task_instance'].xcom_push(key='calc_result', value=result)
    return "calc add"

def calc_mul(x, y, **kwargs):
    result = x * y
    print("x * y : ", result)
    kwargs['task_instance'].xcom_push(key='calc_result', value=result)
    return "calc mul"

def print_result(**kwargs):
    r = kwargs["task_instance"].xcom_pull(key='calc_result')
    print("message : ", r)
    print("*"*100)
    print(kwargs)

def end_seq():
    print("end")

with DAG(
    dag_id="dags_bash_operator2",                              
    schedule="0 0 * * *",                                     
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"),
    catchup=False,
) as dag:
    start = BashOperator(
        task_id='start',
        bash_command='echo "start!"',
    )

    branch = BranchPythonOperator(
        task_id='branch',
        python_callable=random_branch_path,
    )
    
    calc_add = PythonOperator(
        task_id='cal_a_id',
        python_callable=calc_add,
        op_kwargs={'x': 10, 'y':4}
    )

    calc_mul = PythonOperator(
        task_id='cal_m_id',
        python_callable=calc_mul,
        op_kwargs={'x': 10, 'y':4}
    )

    msg = PythonOperator(
        task_id='msg',
        python_callable=print_result,
        trigger_rule=TriggerRule.NONE_FAILED
    )

    complete_py = PythonOperator(
        task_id='complete_py',
        python_callable=end_seq,
        trigger_rule=TriggerRule.NONE_FAILED
    )

    complete = BashOperator(
        task_id='complete_bash',
        depends_on_past=False,
        bash_command='echo "complete~!"',
        trigger_rule=TriggerRule.NONE_FAILED
    )


    start >> branch >> calc_add >> msg >> complete_py >> complete
    start >> branch >> calc_mul >> msg >> complete