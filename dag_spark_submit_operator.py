import logging, json, oracledb
from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator


debug = Variable.get("debug")

logger = logging.getLogger(__name__)


def load_cutoff(cs, **kwargs):
    ti = kwargs['ti']
    dag_id = kwargs['run_id']
    table_names = Variable.get("cutoff_" + str(dag_id), deserialize_json=True)
    # for example We have Service One Service Two and this
    # is for Service One table_names  = '{"service_one": "example_service",  "tables": ["a","b","c","d","e","f]}'

    try:
        connection = oracledb.connect(cs)
        cutoff_data = {
            "tables": []
        }
        with connection.cursor() as cursor:
            tables = tuple(i for i in table_names['tables'])
            # CUTOFF_TABLE_NAME = your cutoff table from any database you want (in this case i use oracle "don't use oracle :D")
            sql = (
                f'select * from CUTOFF_TABLE_NAME where table_name in {tables} ')
            cutoff = cursor.execute(sql)
            for i in cutoff:
                cutoff_data.append(
                    {
                        "table_name": i[0],
                        "cutoff_time": i[1],
                        "cutoff_id": i[2]
                    }
                )        
        ti.xcom_push(key='cutoff_'+str(dag_id),
                        value=json.dumps(cutoff_data))
        message = {"cutoff_xcom": "pushed"}
        logger.info(str(message))
        return "data_pushed_to_xcom"
    except Exception as e:
        message = {"load_cutoff_error": str(e)}
        logger.info(str(message))


# you have to add your envs in Variables in Airflow pannel (Admin Section)
# data info {dag_id }

dag_info_data = Variable.get('your_task_env', deserialize_json=True)


if debug == 'true':
    info = {
        "dag_id": 'your_dag_id_dev',
        "description": 'example dag for development env',
        "start_date": datetime(2023, 8, 15, 4),
        "is_paused_upon_creation": True,
        "jars": 'your custom jars for spark jobs',
        # for examle "jars": 'PATH/mssql-jdbc-12.2.0.jre8.jar,PATH/ojdbc8.jar'
        # for use mssql and oracle connection 
        "owner": 'dag owner name',
        "schedule_interval": '@once'
        # in development mode we set once because it's development and we want to run and debug our dag :D
    }
else:
    info = {
        "dag_id": 'your_dag_id_production',
        "description": 'example dag for development env',
        "start_date": datetime(2023, 8, 15, 4),
        "is_paused_upon_creation": False,
        "jars": 'your custom jars for spark jobs',
        # for examle "jars": 'PATH/mssql-jdbc-12.2.0.jre8.jar,PATH/ojdbc8.jar'
        # for use mssql and oracle connection 
        "owner": 'dag owner name',
        "schedule_interval": '@once'
        # this is for production and you can setup any schedule you want
    }


default_args = {'owner': info['owner'],
                'depends_on_past': False,
                'retries': 2,
                'retry_delay': timedelta(minutes=5)
                }


with DAG(dag_id=info['dag_id'],
         default_args=default_args,
         description=info['description'],
         start_date=info['start_date'],
         schedule_interval=info['schedule_interval'],
         catchup=False,
         tags=['you_tag'],
         # if you have several dags for a service or product that can be seprated
         # you can set tag for search in airflow pannel 
         is_paused_upon_creation=info['is_paused_upon_creation']
         ) as dag:

    if debug == 'true':
    
        
        start = EmptyOperator(task_id='start_dag_dev_mode')
        
        
        test_dag_dev_mode = SparkSubmitOperator(
            task_id='test_dag_dev_mode',
            conn_id='sparkmaster_test',
            application='./dags/"REPOSITORY_NAME"/spark_test/sample_spark_test.py',
            jars=info['jars'],
            name="spark_task_test_dag_dev_mode"
        )
        end = EmptyOperator(task_id='end_dag_dev_mode')

        dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
        dag.doc_md = """
            Spark Dag For Development Mode and test spark
        """

        start >> test_dag_dev_mode >> end
    else:
        # start_task with empty operator
        start = EmptyOperator(task_id='start_dag_production')

        @task(task_id='load_cutoff_data')
        def load_cutoff_data():
            try:
                db_username = dag_info_data['db_username']
                db_password = dag_info_data['db_password']
                db_ip = dag_info_data['db_ip']
                db_port = dag_info_data['db_port']
                db_service_name = dag_info_data['db_service_name']
                cs = f"{db_username}/{db_password}@{db_ip}:{db_port}/{db_service_name}"
                load_cutoff(cs)
            except Exception as e:
                message = {"task_load_cutoff_error": str(e)}
                logger.info(str(message))


        spark_example_task = SparkSubmitOperator(
            task_id='spark_example_task',
            conn_id='sparkmaster_production',
            application='./dags/"REPOSITORY_NAME"/spark_dag_src/sample_spark_script.py',
            jars=info['jars'],
            name="spark_task_dag_production_mode"
        )

        # end_task
        end = EmptyOperator(task_id='end_dag_production')

        dag.doc_md = __doc__
        dag.doc_md = """
                Spark Dag For Production Mode and use SparkSubmitOperator
            """

        start >> spark_example_task >> end
