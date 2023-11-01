from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
import pendulum

with DAG(
    dag_id="McDrive",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2023, 1, 1, tz="Asia/Seoul"),
    catchup=False,
) as dag : 
    op_bread = BashOperator(
        task_id="bread",
        bash_command='echo "Bread ready"'
    )

    op_patty = BashOperator(
        task_id="patty",
        bash_command='echo "Patty ready"'
    )

    op_sauce = BashOperator(
        task_id="sauce",
        bash_command='echo "Sauce ready"'
    )

    op_lettuce = BashOperator(
        task_id="lettuce",
        bash_command='echo "Lettuce ready"'
    )

    op_cheeze = BashOperator(
        task_id="cheeze",
        bash_command='echo "Cheeze ready"'
    )

    op_pickle = BashOperator(
        task_id="pickle",
        bash_command='echo "Pickle raedy"'
    )

    op_onion = BashOperator(
        task_id="onion",
        bash_command='echo "Onion ready"'
    )

    #####################################################
    #                  Drive Through                    #
    #####################################################
    op_visit = BashOperator(
        task_id="visit",
        bash_command='echo "McDonald Visit"'
    )

    op_order = BashOperator(
        task_id="order",
        bash_command='echo "Order"'
    )

    op_pay = BashOperator(
        task_id="pay",
        bash_command='echo "Pay"'
    )

    op_takeOut = BashOperator(
        task_id="take_out",
        bash_command='echo "Take Out"'
    )

    op_pay = BashOperator(
        task_id="pay",
        bash_command='echo "Pay"'
    )

    op_finish = BashOperator(
        task_id="finish",
        bash_command='echo "Pay"'
    )

    op_visit >> op_order >> op_pay >> op_bread
    op_bread >> op_patty >> op_sauce >> op_lettuce >> op_pickle >> op_cheeze >> op_onion



