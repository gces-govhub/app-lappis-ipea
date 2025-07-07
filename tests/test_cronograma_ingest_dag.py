from unittest.mock import patch
from airflow_lappis.dags.data_ingest.cronograma_ingest_dag import dag_instance as dag


def test_dag_loaded():
    assert dag.dag_id == "api_cronogramas_dag"
    assert "fetch_cronogramas" in [t.task_id for t in dag.tasks]
    assert len(dag.tasks) == 1


@patch(
    "airflow_lappis.plugins.cliente_contratos.ClienteContratos.get_cronograma_by_contrato_id"
)
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.drop_table_if_exists")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.get_contratos_ids")
@patch("airflow_lappis.dags.data_ingest.cronograma_ingest_dag.get_postgres_conn")
def test_fetch_cronogramas_success(
    mock_get_postgres_conn,
    mock_get_contratos_ids,
    mock_drop_table,
    mock_insert_data,
    mock_get_cronograma,
):
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_contratos_ids.return_value = [111, 222]
    mock_get_cronograma.return_value = [{"id": 1, "descricao": "Etapa A"}]

    task = dag.get_task("fetch_cronogramas")
    task.execute(context={})

    assert mock_get_contratos_ids.called
    assert mock_drop_table.called
    assert mock_get_cronograma.call_count == 2
    assert mock_insert_data.called
