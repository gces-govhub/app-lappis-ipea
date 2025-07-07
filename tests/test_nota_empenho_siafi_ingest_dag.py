import yaml
from unittest.mock import patch
from airflow_lappis.dags.data_ingest.nota_empenho_siafi_ingest_dag import (
    dag_instance as dag,
)


def test_dag_loaded():
    assert dag.dag_id == "nota_empenho_siafi_ingest_dag"
    assert "fetch_and_store_notas_empenho" in [t.task_id for t in dag.tasks]


@patch("airflow_lappis.plugins.cliente_siafi.ClienteSiafi.consultar_nota_empenho")
@patch("airflow_lappis.plugins.cliente_postgres.ClientPostgresDB.insert_data")
@patch("airflow_lappis.dags.data_ingest.nota_empenho_siafi_ingest_dag.get_postgres_conn")
@patch("airflow.models.Variable.get")
def test_fetch_and_store_notas_empenho_success(
    mock_variable_get,
    mock_get_postgres_conn,
    mock_insert_data,
    mock_consultar_nota_empenho,
):
    task = dag.get_task("fetch_and_store_notas_empenho")

    def variable_side_effect(key, default_var=None):
        if key == "airflow_orgao":
            return "orgao_exemplo"
        elif key == "airflow_variables":
            return yaml.dump({"orgao_exemplo": {"codigos_ug": ["123456"]}})
        return default_var

    mock_variable_get.side_effect = variable_side_effect
    mock_get_postgres_conn.return_value = "postgres://fake_conn"

    def consulta_side_effect(ug, ano, num):
        return {"numEmpenho": num, "anoEmpenho": ano} if int(num) <= 2 else None

    mock_consultar_nota_empenho.side_effect = consulta_side_effect

    task.execute(context={})

    assert mock_consultar_nota_empenho.call_count == 9  # 3 anos × 3 chamadas cada
    assert mock_insert_data.call_count == 6  # 3 anos × 2 inserções por ano
