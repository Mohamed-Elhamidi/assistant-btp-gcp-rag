import re
import unicodedata
from docs_btp import FICHES_BTP


def normaliser(texte: str) -> str:
    """Supprime les accents pour permettre la comparaison sans accent (tranchee == tranchées)."""
    return unicodedata.normalize("NFD", texte).encode("ascii", "ignore").decode()


def _mots_cles(texte: str) -> set[str]:
    """Extrait les mots significatifs (au moins 3 caractères) en minuscules, sans accents."""
    texte_normalise = normaliser(texte.lower())
    mots = re.findall(r"[a-z0-9-]+", texte_normalise)
    return {m for m in mots if len(m) >= 3}


def rechercher_fiches(question: str, limite: int = 2) -> list[dict]:
    """Sélectionne les fiches BTP les plus pertinentes selon la question."""
    mots_question = _mots_cles(question)
    fiches_scorees = []

    for fiche in FICHES_BTP:
        texte_fiche = f"{fiche['titre']} {fiche['categorie']} {fiche['contenu']}"
        mots_fiche = _mots_cles(texte_fiche)
        score = len(mots_question & mots_fiche)
        fiches_scorees.append((score, fiche))

    fiches_scorees.sort(key=lambda item: item[0], reverse=True)
    selection = [fiche for score, fiche in fiches_scorees if score > 0][:limite]
    return selection if selection else [FICHES_BTP[0]]


def construire_contexte_rag(question: str, limite: int = 2) -> tuple[str, list[dict]]:
    """Retourne le texte de contexte formaté pour Gemini et la liste des fiches utilisées."""
    fiches_trouvees = rechercher_fiches(question, limite=limite)
    contexte = "\n\n".join(
        f"[{f['id']}] {f['titre']} ({f['categorie']})\n{f['contenu']}"
        for f in fiches_trouvees
    )
    return contexte, fiches_trouvees
