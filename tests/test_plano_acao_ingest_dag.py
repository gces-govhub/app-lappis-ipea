from unittest.mock import patch
from airflow_lappis.dags.data_ingest.plano_acao_ingest_dag import dag_instance as dag


def test_dag_loaded():
    assert dag.dag_id == "api_planos_acao_dag"
    assert "fetch_and_store_planos_acao" in [t.task_id for t in dag.tasks]


@patch("airflow_lappis.plugins.cliente_ted.ClienteTed.get_planos_acao_by_id_programa")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.get_id_programas")
@patch("airflow_lappis.dags.data_ingest.plano_acao_ingest_dag.get_postgres_conn")
def test_fetch_and_store_planos_acao_success(
    mock_get_postgres_conn,
    mock_get_id_programas,
    mock_insert_data,
    mock_get_planos,
):
    task = dag.get_task("fetch_and_store_planos_acao")

    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_id_programas.return_value = [1, 2]
    mock_get_planos.side_effect = [
        [{"id_plano_acao": 101, "nome": "Plano A"}],
        [{"id_plano_acao": 102, "nome": "Plano B"}],
    ]

    task.execute(context={})

    assert mock_get_planos.call_count == 2
    assert mock_insert_data.call_count == 2
