import pytest
from unittest.mock import patch
from airflow_lappis.dags.data_ingest.empenhos_ingest_dag import dag_instance as dag


def test_dag_loaded():
    assert dag.dag_id == "api_empenhos_dag"
    assert "fetch_empenhos" in [t.task_id for t in dag.tasks]
    assert len(dag.tasks) == 1


@patch("cliente_contratos.ClienteContratos.get_empenhos_by_contrato_id")
@patch("cliente_postgres.ClientPostgresDB.insert_data")
@patch("cliente_postgres.ClientPostgresDB.get_contratos_ids")
@patch("airflow_lappis.dags.data_ingest.empenhos_ingest_dag.get_postgres_conn")
def test_fetch_empenhos_success(
    mock_get_postgres_conn,
    mock_get_contratos_ids,
    mock_insert_data,
    mock_get_empenhos,
):
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_contratos_ids.return_value = [101, 202]
    mock_get_empenhos.return_value = [{"id": 1, "descricao": "Empenho A"}]

    task = dag.get_task("fetch_empenhos")
    task.execute(context={})

    assert mock_get_contratos_ids.called
    assert mock_get_empenhos.call_count == 2
    assert mock_insert_data.called
