import pytest
from unittest.mock import patch
from airflow_lappis.dags.data_ingest.programacao_financeira_siafi_ingest_dag import dag_instance as dag


def test_dag_loaded():
    assert dag.dag_id == "programacao_financeira_siafi_dag"
    task_ids = [task.task_id for task in dag.tasks]
    assert "fetch_and_store_programacao_financeira" in task_ids


@patch("airflow_lappis.plugins.cliente_siafi.ClienteSiafi.consultar_programacao_financeira")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.get_programacao_financeira")
@patch("airflow_lappis.dags.data_ingest.programacao_financeira_siafi_ingest_dag.get_postgres_conn")
def test_fetch_and_store_programacao_financeira_success(
    mock_get_postgres_conn,
    mock_get_programacoes,
    mock_insert_data,
    mock_consultar_programacao,
):
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_programacoes.return_value = [("202412345678", "123456")]
    mock_consultar_programacao.return_value = {
        "TRF__numeroDocumento": "202412345678",
        "valor": 1000.0
    }

    task = dag.get_task("fetch_and_store_programacao_financeira")
    result = task.execute(context={})

    assert mock_get_programacoes.called
    assert mock_consultar_programacao.called
    assert mock_insert_data.called
