import os
import sys
import pytest
from airflow.models import DagBag

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(scope="module")
def dag_bag():
    """
    Carrega as DAGs da pasta específica do projeto.
    """
    return DagBag(dag_folder="airflow_lappis/dags/data_ingest", include_examples=False)

def test_dag_loaded(dag_bag):
    """
    Testa se a DAG 'api_contratos_inativos_dag' foi carregada corretamente no DagBag.
    """
    dag_id = "api_contratos_inativos_dag"

    assert dag_id in dag_bag.dags, f"DAG '{dag_id}' não encontrada no DagBag"

    dag = dag_bag.dags[dag_id]
    assert dag is not None

    task_ids = [task.task_id for task in dag.tasks]
    assert "fetch_and_store_contratos_inativos" in task_ids, \
        "'fetch_and_store_contratos_inativos' não encontrada na DAG"
