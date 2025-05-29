import pytest
from unittest.mock import patch, MagicMock
from airflow.models import Variable
from airflow_lappis.dags.data_ingest.estagios_tesouro_ingest_dag import dag


@patch("airflow.models.Variable.get")
@patch("airflow_lappis.dags.data_ingest.estagios_tesouro_ingest_dag.fetch_and_process_email")
def test_process_emails_task(mock_fetch_email, mock_var_get):
    mock_var_get.return_value = '{"email": "x", "password": "y", "imap_server": "z", "sender_email": "w"}'
    mock_fetch_email.return_value = "col1,col2\nval1,val2"

    task = dag.get_task("process_emails")
    result = task.execute(context={})

    assert result == "col1,col2\nval1,val2"


@patch("airflow_lappis.dags.data_ingest.estagios_tesouro_ingest_dag.get_postgres_conn")
@patch("airflow_lappis.dags.data_ingest.estagios_tesouro_ingest_dag.ClientPostgresDB.insert_csv_data")
def test_insert_to_db_task(mock_insert_csv_data, mock_get_postgres_conn):
    mock_get_postgres_conn.return_value = "fake_connection_string"
    mock_insert_csv_data.return_value = None

    task = dag.get_task("insert_to_db")
    mock_context = {
        "ti": MagicMock(xcom_pull=MagicMock(return_value="col1,col2\nval1,val2"))
    }

    task.execute(context=mock_context)

    mock_insert_csv_data.assert_called_once_with("col1,col2\nval1,val2", "estagios_tesouro", schema="siafi")
