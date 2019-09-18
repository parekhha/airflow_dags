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
    from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

    args = {
        'owner': 'Airflow',
        'start_date': days_ago(2)
    }

    dag = DAG(
        dag_id='example_kubernetes_operator',
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

    k = KubernetesPodOperator(
        namespace='default',
        image="ubuntu:16.04",
        cmds=["bash", "-cx"],
        arguments=["echo {{ dag_run.conf['key'] }}"],
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_id="task",
        get_logs=True,
        in_cluster=True,
        dag=dag,
        is_delete_operator_pod=False,
        tolerations=tolerations
    )

except ImportError as e:
    log.warning("Could not import KubernetesPodOperator: " + str(e))
    log.warning("Install kubernetes dependencies with: "
                "    pip install 'apache-airflow[kubernetes]'")
