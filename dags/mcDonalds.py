from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
import pendulum

op_sample = DummyOperator(
    task_id="test",
)

def random_branch_path():
    from random import randint

    return "work_in" if randint(1, 2) == 1 else "drive_through"

def burger_order() : 
    return "burger_start", "pay"

with DAG(
    dag_id="McDrive",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2023, 1, 1, tz="Asia/Seoul"),
    catchup=False,
) as dag : 
    #####################################################
    #                  Burger Recipe                    #
    #####################################################
    op_recipe_start = DummyOperator(
        task_id="burger_start"
    )

    op_recipe_finish = DummyOperator(
        task_id="burger_finish"
    )

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
    
    '''
    op_order = BashOperator(
        task_id="order",
        bash_command='echo "Order"'
    )
    '''
    op_order = BranchPythonOperator(
        task_id="order",
        python_callable=burger_order,
    )

    op_pay = BashOperator(
        task_id="pay",
        bash_command='echo "Pay"'
    )

    op_takeOut = BashOperator(
        task_id="take_out",
        bash_command='echo "Take Out"'
    )

    op_finish = BashOperator(
        task_id="finish",
        bash_command='echo "Finish"'
    )

    '''burger recipe'''
    op_recipe_start >> op_bread >> op_patty >> op_sauce >> op_lettuce >> op_pickle >> op_cheeze >> op_onion >> op_recipe_finish >> op_takeOut

    # op_visit >> op_order >> op_bread
    op_visit >> op_order >> op_recipe_start
    # op_visit >> op_order >> op_pay >> [op_onion, op_takeOut] >> op_finish
    op_visit >> op_order >> op_pay >> op_takeOut >> op_finish



