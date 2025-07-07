import pytest
from unittest.mock import patch
from airflow_lappis.dags.data_ingest.programas_ingest_dag import dag_instance as dag


def test_dag_loaded():
    assert dag.dag_id == "api_programas_dag"
    task_ids = [task.task_id for task in dag.tasks]
    assert "fetch_and_update_programas" in task_ids


@patch("airflow_lappis.plugins.cliente_ted.ClienteTed.get_programa_by_id_programa")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.alter_table")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.get_id_programas")
@patch("airflow_lappis.dags.data_ingest.programas_ingest_dag.get_postgres_conn")
def test_fetch_and_update_programas_success(
    mock_get_postgres_conn,
    mock_get_id_programas,
    mock_alter_table,
    mock_insert_data,
    mock_get_programa_by_id,
):
    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_id_programas.return_value = ["1"]
    mock_get_programa_by_id.return_value = [
        {"id_programa": "1", "nome": "Programa Teste"}
    ]

    task = dag.get_task("fetch_and_update_programas")
    task.execute(context={})

    mock_get_id_programas.assert_called_once()
    mock_get_programa_by_id.assert_called_once_with("1")
    mock_alter_table.assert_called_once_with(
        {"id_programa": "1", "nome": "Programa Teste"},
        "programas",
        schema="transfere_gov",
    )
    mock_insert_data.assert_called_once_with(
        [{"id_programa": "1", "nome": "Programa Teste"}],
        "programas",
        primary_key=["id_programa"],
        conflict_fields=["id_programa"],
        schema="transfere_gov",
    )
