from datetime import datetime, timezone
import os
import uuid
from typing import Any

from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError


def _get_bigquery_config() -> tuple[str, str, str]:
    """Récupère les coordonnées BigQuery depuis les variables d'environnement."""
    project_id = os.getenv("BQ_PROJECT_ID", "gen-lang-client-0106828848")
    dataset_id = os.getenv("BQ_DATASET", "assistant_btp")
    table_id = os.getenv("BQ_TABLE", "journal_questions")
    return project_id, dataset_id, table_id


def enregistrer_echange_bigquery(
    question: str,
    reponse: str,
    sources: list[str] | None = None,
    modele: str = "gemini-2.5-flash",
    latence_ms: int = 0,
) -> dict[str, Any]:
    """
    Insère un échange question/réponse dans BigQuery via une requête SQL paramétrée.
    Équivalent d'une requête SQL préparée (INSERT INTO) exécutée avec client.query().
    """
    event_id = str(uuid.uuid4())
    project_id, dataset_id, table_id = _get_bigquery_config()
    table_fqn = f"`{project_id}.{dataset_id}.{table_id}`"

    # Formate la liste des sources en chaîne lisible (ex: "FICHE-01, FICHE-02")
    sources_str = ", ".join(sources) if sources else ""

    # Horodatage UTC actuel pour la colonne TIMESTAMP
    created_at = datetime.now(timezone.utc)

    sql = f"""
        INSERT INTO {table_fqn} (
            event_id,
            question,
            reponse,
            sources,
            modele,
            latence_ms,
            created_at
        )
        VALUES (
            @event_id,
            @question,
            @reponse,
            @sources,
            @modele,
            @latence_ms,
            @created_at
        )
    """

    # Paramètres typés (équivalent des paramètres liés en SQL préparé)
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("event_id", "STRING", event_id),
            bigquery.ScalarQueryParameter("question", "STRING", question),
            bigquery.ScalarQueryParameter("reponse", "STRING", reponse),
            bigquery.ScalarQueryParameter("sources", "STRING", sources_str),
            bigquery.ScalarQueryParameter("modele", "STRING", modele),
            bigquery.ScalarQueryParameter("latence_ms", "INT64", int(latence_ms)),
            bigquery.ScalarQueryParameter("created_at", "TIMESTAMP", created_at),
        ]
    )

    try:
        # Utilise les Application Default Credentials (ADC) ou le compte de service GCP
        client = bigquery.Client(project=project_id)

        # Exécute la requête INSERT et attend la fin du job BigQuery
        query_job = client.query(sql, job_config=job_config)
        query_job.result()

        return {
            "ok": True,
            "event_id": event_id,
            "table": f"{project_id}.{dataset_id}.{table_id}",
        }
    except GoogleCloudError as exc:
        return {
            "ok": False,
            "event_id": event_id,
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "ok": False,
            "event_id": event_id,
            "error": str(exc),
        }