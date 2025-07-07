from airflow_lappis.dags.data_ingest.faturas_ingest_dag import dag_instance as dag
from unittest.mock import patch


def test_dag_loaded():
    assert dag.dag_id == "api_faturas_dag"
    task_ids = [task.task_id for task in dag.tasks]
    assert "fetch_faturas" in task_ids


@patch(
    "airflow_lappis.plugins.cliente_contratos.ClienteContratos.get_faturas_by_contrato_id"
)
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.get_contratos_ids")
@patch("airflow_lappis.dags.data_ingest.faturas_ingest_dag.get_postgres_conn")
def test_fetch_faturas_success(
    mock_get_postgres_conn,
    mock_get_contratos_ids,
    mock_insert_data,
    mock_get_faturas,
):
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_contratos_ids.return_value = [111, 222]
    mock_get_faturas.return_value = [
        {"id": 1, "descricao": "Fatura A"},
        {"id": 2, "descricao": "Fatura B"},
    ]

    task = dag.get_task("fetch_faturas")
    task.execute(context={})

    assert mock_get_contratos_ids.called
    assert mock_get_faturas.call_count == 2
    assert mock_insert_data.call_count == 2
