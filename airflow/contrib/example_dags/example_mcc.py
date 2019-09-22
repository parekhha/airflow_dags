"""
This is an example dag for using the KubernetesPodOperator.
"""
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.models import DAG

log = LoggingMixin().log

try:
    # Kubernetes is optional, so not available in vanilla Airflow
    # pip install 'apache-airflow[kubernetes]'
    from airflow_plugin_demo.plugins.glhc_operator import GLHCOperator

    args = {
        'owner': 'Airflow',
        'start_date': days_ago(2)
    }

    dag = DAG(
        dag_id='example_mcc',
        default_args=args,
        schedule_interval=None
    )

    tolerations = [
        {
            'key': "key",
            'operator': 'Equal',
            'value': 'value'
        }
    ]

    serviceNow = GLHCOperator(
        namespace='default',
        image="ubuntu:16.04",
        cmds=["bash", "-cx"],
        arguments=["echo {{ dag_run.conf['key'] }}; sleep 5"],
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_description="Configuring Service Now",
        task_id="service_now",
        get_logs=True,
        in_cluster=True,
        dag=dag,
        is_delete_operator_pod=False,
        tolerations=tolerations
    )
    
    opsRam = GLHCOperator(
        namespace='default',
        image="ubuntu:16.04",
        cmds=["bash", "-cx"],
        arguments=["echo {{ dag_run.conf['key'] }}; sleep 5"],
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_description="Configuring Ops ram",
        task_id="ops_ram",
        get_logs=True,
        in_cluster=True,
        dag=dag,
        is_delete_operator_pod=False,
        tolerations=tolerations
    )
    
    mcc = GLHCOperator(
        namespace='default',
        image="ubuntu:16.04",
        cmds=["bash", "-cx"],
        arguments=["echo {{ dag_run.conf['key'] }}; sleep 5"],
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_description="Configuring mcc",
        task_id="mcc",
        get_logs=True,
        in_cluster=True,
        dag=dag,
        is_delete_operator_pod=False,
        tolerations=tolerations
    )
    serviceNow >> opsRam >> mcc 
except ImportError as e:
    log.warning("Could not import KubernetesPodOperator: " + str(e))
    log.warning("Install kubernetes dependencies with: "
                "    pip install 'apache-airflow[kubernetes]'")
