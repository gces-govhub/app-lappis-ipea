import logging
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow_lappis.helpers.postgres_helpers import get_postgres_conn
from airflow_lappis.plugins.cliente_contratos import ClienteContratos
from airflow_lappis.plugins.cliente_postgres import ClientPostgresDB


@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        "owner": "Davi",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["empenhos_api"],
)
def api_empenhos_dag() -> None:
    """DAG para buscar e armazenar empenhos de uma API no PostgreSQL."""

    @task
    def fetch_empenhos() -> None:
        logging.info("[empenhos_ingest_dag.py] Starting fetch_empenhos task")
        api = ClienteContratos()
        postgres_conn_str = get_postgres_conn()
        db = ClientPostgresDB(postgres_conn_str)
        contratos_ids = db.get_contratos_ids()

        for contrato_id in contratos_ids:
            try:
                logging.info(
                    f"[empenhos_ingest_dag.py] Fetching empenhos for contrato ID: "
                    f"{contrato_id}"
                )
                empenhos = api.get_empenhos_by_contrato_id(str(contrato_id))

                if empenhos:
                    for empenho in empenhos:
                        empenho["contrato_id"] = contrato_id

                logging.info(
                    f"[empenhos_ingest_dag.py] Inserting empenhos for contrato ID: "
                    f"{contrato_id} into PostgreSQL"
                )
                db.insert_data(
                    empenhos,
                    "empenhos",
                    conflict_fields=["id", "contrato_id"],
                    primary_key=["id", "contrato_id"],
                    schema="compras_gov",
                )
            except Exception as e:
                logging.error(
                    f"[empenhos_ingest_dag.py] Error fetching empenhos for contrato "
                    f"ID {contrato_id}: {e}"
                )

    fetch_empenhos()


dag_instance = api_empenhos_dag()
