import pytest
from unittest.mock import patch
from airflow_lappis.dags.data_ingest.unidade_organizacional_ingest_dag import dag_instance as dag

def test_dag_loaded():
    assert dag.dag_id == "api_unidade_organizacional_dag"
    task_ids = [task.task_id for task in dag.tasks]
    assert "fetch_estrutura_organizacional_resumida" in task_ids


@patch("cliente_estrutura.ClienteEstrutura.get_estrutura_organizacional_resumida")
@patch("cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.dags.data_ingest.unidade_organizacional_ingest_dag.get_postgres_conn")
def test_fetch_estrutura_organizacional_resumida_success(
    mock_get_postgres_conn,
    mock_insert_data,
    mock_get_estrutura,
):
    task = dag.get_task("fetch_estrutura_organizacional_resumida")

    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_estrutura.return_value = [
        {"codigoUnidade": "7", "nomeUnidade": "Unidade Teste"}
    ]

    task.execute(context={})

    mock_get_estrutura.assert_called_once_with(
        codigo_poder="1",
        codigo_esfera="1",
        codigo_unidade="7"
    )
    mock_insert_data.assert_called_once_with(
        [{"codigoUnidade": "7", "nomeUnidade": "Unidade Teste"}],
        "unidade_organizacional",
        conflict_fields=["codigoUnidade"],
        primary_key=["codigoUnidade"],
        schema="siorg",
    )
