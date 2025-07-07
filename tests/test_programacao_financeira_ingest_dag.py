import pytest
import yaml
from unittest.mock import patch, MagicMock
from airflow_lappis.dags.data_ingest.programacao_financeira_ingest_dag import (
    dag_instance as dag,
)


def test_dag_loaded():
    assert dag.dag_id == "programacao_financeira_dag"
    assert "fetch_and_store_programacao_financeira" in [t.task_id for t in dag.tasks]


@patch("airflow_lappis.plugins.cliente_ted.ClienteTed.get_programacao_financeira_by_ug")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch(
    "airflow_lappis.dags.data_ingest.programacao_financeira_ingest_dag.get_postgres_conn"
)
@patch("airflow.models.Variable.get")
def test_fetch_and_store_programacao_financeira_success(
    mock_variable_get,
    mock_get_postgres_conn,
    mock_insert_data,
    mock_get_programacao,
):
    task = dag.get_task("fetch_and_store_programacao_financeira")

    def variable_side_effect(key, default_var=None):
        if key == "airflow_orgao":
            return "orgao_exemplo"
        elif key == "airflow_variables":
            return yaml.dump({"orgao_exemplo": {"codigos_ug": ["123456"]}})
        return default_var

    mock_variable_get.side_effect = variable_side_effect
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_programacao.return_value = [
        {"id_programacao": "prog1", "valor": 150.0},
        {"id_programacao": "prog2", "valor": 300.0},
    ]

    task.execute(context={})

    mock_get_programacao.assert_called_once_with("123456")
    assert mock_insert_data.called
