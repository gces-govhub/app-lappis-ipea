import pytest
from unittest.mock import patch
from airflow_lappis.dags.data_ingest.programa_beneficiario_ingest_dag import (
    dag_instace as dag,
)


def test_dag_loaded():
    assert dag.dag_id == "api_programa_beneficiario_dag"
    assert "fetch_and_store_programa_beneficiario" in [t.task_id for t in dag.tasks]


@patch("airflow_lappis.plugins.cliente_ted.ClienteTed.get_ted_by_programa_beneficiario")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch(
    "airflow_lappis.dags.data_ingest.programa_beneficiario_ingest_dag.get_postgres_conn"
)
def test_fetch_and_store_programa_beneficiario_success(
    mock_get_postgres_conn,
    mock_insert_data,
    mock_get_beneficiario,
):
    task = dag.get_task("fetch_and_store_programa_beneficiario")

    mock_get_postgres_conn.return_value = "postgres://fake_conn"
    mock_get_beneficiario.return_value = [
        {"id_programa": "1", "nome": "Programa A"},
        {"id_programa": "2", "nome": "Programa B"},
        {"id_programa": "1", "nome": "Programa A"},
    ]

    task.execute(context={})

    mock_get_beneficiario.assert_called_once_with("7")
    call_args = mock_insert_data.call_args
    inserted_data = call_args[0][0]  # primeiro argumento posicional: os dados inseridos

    # Verifica que os dados esperados estão presentes, independentemente da ordem
    expected_data = [{"id_programa": "1"}, {"id_programa": "2"}]
    assert sorted(inserted_data, key=lambda x: x["id_programa"]) == sorted(
        expected_data, key=lambda x: x["id_programa"]
    )

    # Verifica os outros argumentos
    assert call_args[0][1] == "programas"
    assert call_args.kwargs["primary_key"] == ["id_programa"]
    assert call_args.kwargs["conflict_fields"] == ["id_programa"]
    assert call_args.kwargs["schema"] == "transfere_gov"
