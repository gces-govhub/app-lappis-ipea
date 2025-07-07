from airflow_lappis.dags.data_ingest.nota_credito_siafi_ingest_dag import (
    dag_instance as dag,
)
from unittest.mock import patch


def test_dag_loaded():
    assert dag.dag_id == "nota_credito_siafi_dag"
    task_ids = [task.task_id for task in dag.tasks]
    assert "fetch_and_store_nota_credito" in task_ids


@patch("airflow_lappis.plugins.cliente_siafi.ClienteSiafi.consultar_nota_credito")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.get_nota_credito")
@patch("airflow_lappis.dags.data_ingest.nota_credito_siafi_ingest_dag.get_postgres_conn")
def test_fetch_and_store_nota_credito_success(
    mock_get_postgres_conn,
    mock_get_nota_credito,
    mock_insert_data,
    mock_consultar_nota_credito,
):
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_nota_credito.return_value = [("110000", "170001", "202312345678")]
    mock_consultar_nota_credito.return_value = {"numero": "123456", "valor": 100.0}

    task = dag.get_task("fetch_and_store_nota_credito")
    task.execute(context={})

    assert mock_get_nota_credito.called
    assert mock_consultar_nota_credito.called
    assert mock_insert_data.called
