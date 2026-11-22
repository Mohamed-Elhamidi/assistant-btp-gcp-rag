from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from rag_btp import construire_contexte_rag

# Charge GEMINI_API_KEY depuis le fichier .env
load_dotenv()

# Initialise le client Gemini
client = genai.Client()

MODELES_CANDIDATS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]

SYSTEM_INSTRUCTION = """
Tu es un assistant technique spécialisé dans le secteur du BTP (Bâtiment et Travaux Publics) en France.
Ton objectif est d'aider les professionnels et apprentis sur les bonnes pratiques, la prévention des risques et les normes de sécurité chantier.

Règles strictes :
1. Appuie-toi en priorité sur les FICHES DOCUMENTAIRES fournies dans le contexte.
2. Si une information n'est pas présente dans les fiches fournies, dis-le clairement au lieu d'inventer.
3. Réponds en français clair, structuré et actionnable, et rappelle toujours de vérifier le PPSPS / plan de prévention et la réglementation en vigueur.
"""


def _generer_avec_repli(prompt: str):
    """Essaie les modèles candidats et bascule si un modèle est temporairement indisponible (503)."""
    dernier_erreur = None
    for modele in MODELES_CANDIDATS:
        try:
            response = client.models.generate_content(
                model=modele,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.3,
                ),
            )
            return response, modele
        except ServerError as err:
            dernier_erreur = err
            print(f"[Info] Modèle '{modele}' indisponible ({err.code}), essai du suivant...")
    raise dernier_erreur


def repondre_btp(question: str) -> tuple[str, list[dict]]:
    """Récupère le contexte RAG pertinent puis génère la réponse avec Gemini."""
    contexte, fiches_utilisees = construire_contexte_rag(question)

    prompt = f"""FICHES DOCUMENTAIRES :
{contexte}

QUESTION UTILISATEUR :
{question}
"""

    response, _modele_utilise = _generer_avec_repli(prompt)
    return response.text or "", fiches_utilisees


if __name__ == "__main__":
    question_test = "Quelles précautions prendre pour creuser une tranchée sans risque d'éboulement ?"
    reponse, fiches = repondre_btp(question_test)

    print("Fiches utilisées :", [f["id"] for f in fiches])
    print("-" * 50)
    print(reponse)