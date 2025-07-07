import pytest
import yaml
from unittest.mock import patch
from airflow_lappis.dags.data_ingest.notas_de_credito_ingest_dag import (
    dag_instance as dag,
)


def test_dag_loaded():
    assert dag.dag_id == "notas_de_credito_dag"
    assert "fetch_and_store_notas_de_credito" in [t.task_id for t in dag.tasks]


@patch("airflow_lappis.plugins.cliente_ted.ClienteTed.get_notas_de_credito_by_ug")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.dags.data_ingest.notas_de_credito_ingest_dag.get_postgres_conn")
@patch("airflow.models.Variable.get")
def test_fetch_and_store_notas_de_credito_success(
    mock_variable_get,
    mock_get_postgres_conn,
    mock_insert_data,
    mock_get_notas,
):
    task = dag.get_task("fetch_and_store_notas_de_credito")

    def variable_side_effect(key, default_var=None):
        if key == "airflow_orgao":
            return "orgao_exemplo"
        elif key == "airflow_variables":
            return yaml.dump({"orgao_exemplo": {"codigos_ug": ["123456"]}})
        return default_var

    mock_variable_get.side_effect = variable_side_effect
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_notas.return_value = [
        {"id_nota": "nota1", "valor": 100.0},
        {"id_nota": "nota2", "valor": 200.0},
    ]

    task.execute(context={})

    mock_get_notas.assert_called_once_with("123456")
    assert mock_insert_data.called
