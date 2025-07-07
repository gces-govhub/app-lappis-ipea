import yaml
from airflow_lappis.dags.data_ingest.contratos_inativos_ingest_dag import (
    dag_instance as dag,
)
from unittest.mock import patch


def test_dag_loaded():
    assert dag.dag_id == "api_contratos_inativos_dag"
    task_ids = [t.task_id for t in dag.tasks]

    assert "fetch_and_store_contratos_inativos" in task_ids
    assert len(task_ids) == 1


@patch(
    "airflow_lappis.plugins.cliente_contratos.ClienteContratos.get_contratos_inativos_by_ug"
)
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.dags.data_ingest.contratos_inativos_ingest_dag.get_postgres_conn")
@patch("airflow.models.Variable.get")
def test_fetch_and_store_contratos_inativos_success(
    mock_variable_get,
    mock_get_postgres_conn,
    mock_insert_data,
    mock_get_contratos_inativos_by_ug,
):
    def variable_side_effect(key, default_var=None):
        if key == "airflow_orgao":
            return "orgao_exemplo"
        elif key == "airflow_variables":
            return yaml.dump({"orgao_exemplo": {"codigos_ug": ["111111", "222222"]}})
        return default_var

    mock_variable_get.side_effect = variable_side_effect
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_contratos_inativos_by_ug.return_value = [{"id": 10, "campo": "valor"}]

    task = dag.get_task("fetch_and_store_contratos_inativos")
    task.execute(context={})

    assert mock_get_contratos_inativos_by_ug.call_count == 2
    assert mock_insert_data.called
