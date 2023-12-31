from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
import pendulum

def hello_airflow() : 
    print("hello_airflow")

with DAG(
    dag_id="dag_simple_example",                                
    schedule="0 0 * * *",                                       
    start_date=pendulum.datetime(2023, 10, 1, tz="Asia/Seoul"), 
    catchup=False,                                              
) as dag : 
    op_start = BashOperator(
        task_id="op_start",
        bash_command='echo "start!"',
        trigger_rule=TriggerRule.NONE_FAILED,
    )

    op_print_msg = PythonOperator(
        task_id="op_print_msg",
        python_callable=hello_airflow,
    )

    op_end = BashOperator(
        task_id="op_end",
        bash_command='echo "complete!"',
        trigger_rule=TriggerRule.NONE_FAILED,
    )

    op_start >> op_print_msg >> op_end