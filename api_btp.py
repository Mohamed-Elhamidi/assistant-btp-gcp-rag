from fastapi import FastAPI
from pydantic import BaseModel
from assistant_btp import repondre_btp
from journal_btp import enregistrer_echange

app = FastAPI(
    title="Assistant BTP - API RAG",
    description="API de questions/réponses sécurité chantier basée sur les fiches BTP.",
    version="0.1.0",
)


class QuestionRequest(BaseModel):
    question: str


class FicheSource(BaseModel):
    id: str
    titre: str
    categorie: str


class ReponseBTP(BaseModel):
    reponse: str
    fiches_utilisees: list[FicheSource]


@app.get("/health")
def health_check():
    """Route simple pour vérifier que l'API répond bien."""
    return {"status": "ok"}


@app.post("/ask", response_model=ReponseBTP)
def poser_question_api(payload: QuestionRequest):
    """Reçoit une question JSON et retourne la réponse RAG + les fiches utilisées."""
    reponse_texte, fiches = repondre_btp(payload.question)
    sources = [
        FicheSource(
            id=f["id"],
            titre=f["titre"],
            categorie=f["categorie"],
        )
        for f in fiches
    ]

    enregistrer_echange(
        question=payload.question,
        reponse=reponse_texte,
        fiches=fiches,
    )
    return ReponseBTP(reponse=reponse_texte, fiches_utilisees=sources)