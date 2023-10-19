from airflow import DAG
# from airflow.operators.bash import BashOperator
import datetime
import pendulum

with DAG(
    dag_id="dags_bash_operator",                                # DAG ID 
    schedule="0 0 * * *",                                       # 분 시 일 월 요일    
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"),  # 시간 기준
    catchup=False,
    #dagrun_timeout=datetime.timedelta(minutes=60),
) as dag : 
    bash_t1 = BashOperator(
        task_id="bash_t1",                                      # Task 이름 
        bash_command="echo whoami",
    )

    bash_t2 = BashOperator(
        task_id="bash_t2",                                      # Task 이름 
        bash_command="echo $HOSTNAME",                          # WSL HOSTNAME
    )

    bash_t1 >> bash_t2                                          # 수행 순서 

