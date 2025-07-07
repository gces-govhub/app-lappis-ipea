from unittest.mock import patch, MagicMock
from airflow_lappis.dags.data_ingest.empenhos_tesouro_ingest_dag import dag


def test_dag_loaded():
    assert dag.dag_id == "email_empenhos_tesouro_ingest"
    assert "process_emails" in [t.task_id for t in dag.tasks]
    assert "insert_to_db" in [t.task_id for t in dag.tasks]
    assert len(dag.tasks) == 2


@patch("airflow.models.Variable.get")
@patch(
    "airflow_lappis.dags.data_ingest.empenhos_tesouro_ingest_dag.fetch_and_process_email"
)
def test_process_emails_task(mock_fetch_email, mock_var_get):
    mock_var_get.return_value = (
        '{"email": "x", "password": "y", "imap_server": "z", "sender_email": "w"}'
    )
    mock_fetch_email.return_value = "col1,col2\nval1,val2"

    task = dag.get_task("process_emails")
    result = task.execute(context={})

    assert result == "col1,col2\nval1,val2"
    assert mock_fetch_email.called


@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch(
    "airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.__init__", return_value=None
)
@patch("airflow_lappis.dags.data_ingest.empenhos_tesouro_ingest_dag.get_postgres_conn")
@patch("airflow.models.Variable.get")
def test_insert_to_db_task(mock_var_get, mock_get_conn, mock_db_init, mock_insert_data):
    context = {"ti": MagicMock()}
    csv_content = (
        "ne_ccor,natureza_despesa,doc_observacao,ne_ccor_ano_emissao,"
        "emissao_dia,emissao_mes\n"
        "abc,123,obs,2024,01,01"
    )
    context["ti"].xcom_pull.return_value = csv_content

    mock_get_conn.return_value = "postgres://fake"
    task = dag.get_task("insert_to_db")
    task.execute(context=context)

    assert mock_insert_data.called
