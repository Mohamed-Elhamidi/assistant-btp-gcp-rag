import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "journal_btp.db"


def initialiser_journal() -> None:
    """Crée la table SQLite du journal si elle n'existe pas encore."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS journal_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_creation TEXT NOT NULL,
                question TEXT NOT NULL,
                reponse TEXT NOT NULL,
                fiches_ids TEXT NOT NULL
            )
            """
        )
        conn.commit()


def enregistrer_echange(question: str, reponse: str, fiches: list[dict]) -> None:
    """Enregistre une question, sa réponse et les fiches BTP mobilisées."""
    initialiser_journal()
    fiches_ids = ", ".join(f["id"] for f in fiches) if fiches else "AUCUNE"
    date_iso = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO journal_questions (date_creation, question, reponse, fiches_ids)
            VALUES (?, ?, ?, ?)
            """,
            (date_iso, question, reponse, fiches_ids),
        )
        conn.commit()