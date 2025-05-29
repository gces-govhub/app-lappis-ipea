import pytest
import pandas as pd
import io
from unittest.mock import patch, MagicMock
from airflow_lappis.dags.data_ingest.pf_tesouro_ingest_dag import dag as dag_instance


def test_dag_loaded():
    assert dag_instance.dag_id == "email_programacoes_financeiras_ingest"
    expected_tasks = [
        "process_emails_enviadas",
        "process_emails_recebidas",
        "combine_data",
        "insert_to_db",
        "clean_duplicates",
    ]
    task_ids = [t.task_id for t in dag_instance.tasks]
    for task_id in expected_tasks:
        assert task_id in task_ids


@patch("cliente_email.fetch_and_process_email")
@patch("cliente_postgres.ClientPostgresDB.insert_data")
@patch("cliente_postgres.ClientPostgresDB.remove_duplicates")
@patch("airflow.models.Variable.get")
@patch("airflow_lappis.dags.data_ingest.pf_tesouro_ingest_dag.get_postgres_conn")
def test_email_pf_pipeline_success(
    mock_get_postgres_conn,
    mock_variable_get,
    mock_remove_duplicates,
    mock_insert_data,
    mock_fetch_email,
):
    enviadas_data = [
        {"emissao_mes": "01", "ug_emitente": "123456", "pf_valor_linha": 100.0},
    ]
    recebidas_data = [
        {"pf_valor_linha": 200.0},
    ]

    def variable_side_effect(key, default_var=None):
        if key == "email_credentials":
            return '{"email": "x", "password": "x", "imap_server": "x", "sender_email": "x"}'
        return default_var

    mock_variable_get.side_effect = variable_side_effect
    mock_fetch_email.side_effect = [enviadas_data, recebidas_data]
    mock_get_postgres_conn.return_value = "postgres://fake_conn"

    task_enviadas = dag_instance.get_task("process_emails_enviadas")
    task_recebidas = dag_instance.get_task("process_emails_recebidas")
    task_combine = dag_instance.get_task("combine_data")
    task_insert = dag_instance.get_task("insert_to_db")
    task_clean = dag_instance.get_task("clean_duplicates")

    context = {"ti": MagicMock()}
    combined_df = pd.DataFrame(enviadas_data + recebidas_data)
    csv_string = combined_df.to_csv(index=False)
    context["ti"].xcom_pull.side_effect = [enviadas_data, recebidas_data, csv_string]

    task_enviadas.execute(context={})
    task_recebidas.execute(context={})
    task_combine.execute(context=context)
    task_insert.execute(context=context)
    task_clean.execute(context={})

    assert mock_insert_data.called
    assert mock_remove_duplicates.called
