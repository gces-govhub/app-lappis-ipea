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
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["cronogramas_api"],
)
def api_cronogramas_dag() -> None:
    """DAG para buscar e armazenar cronogramas de uma API no PostgreSQL."""

    @task
    def fetch_cronogramas() -> None:
        logging.info("[cronograma_ingest_dag.py] Starting fetch_cronogramas task")
        api = ClienteContratos()
        postgres_conn_str = get_postgres_conn()
        db = ClientPostgresDB(postgres_conn_str)
        contratos_ids = db.get_contratos_ids()

        # Drop the existing cronograma table before inserting new data
        logging.info("[cronograma_ingest_dag.py] Dropping existing cronograma table")
        db.drop_table_if_exists("cronograma", schema="compras_gov")
        logging.info("[cronograma_ingest_dag.py] Table dropped successfully")

        for contrato_id in contratos_ids:
            logging.info(
                f"[cronograma_ingest_dag.py] Fetching cronograma for contrato ID: "
                f"{contrato_id}"
            )
            cronograma = api.get_cronograma_by_contrato_id(contrato_id)
            if cronograma:
                logging.info(
                    f"[cronograma_ingest_dag.py] Inserting cronograma for contrato ID: "
                    f"{contrato_id} into PostgreSQL"
                )
                db.insert_data(
                    cronograma,
                    "cronograma",
                    conflict_fields=["id"],
                    primary_key=["id"],
                    schema="compras_gov",
                )
            else:
                logging.warning(
                    f"[cronograma_ingest_dag.py] No cronograma found for contrato ID: "
                    f"{contrato_id}"
                )

    fetch_cronogramas()


dag_instance = api_cronogramas_dag()
