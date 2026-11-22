import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Charge les variables d'environnement depuis le fichier .env (ex: GEMINI_API_KEY)
load_dotenv()

# Initialise le client Gemini (il lit automatiquement GEMINI_API_KEY dans l'environnement)
client = genai.Client()

# Instruction système : définit le rôle, le ton et les limites de l'assistant BTP
SYSTEM_INSTRUCTION = """
Tu es un assistant technique spécialisé dans le secteur du BTP (Bâtiment et Travaux Publics) en France.
Ton objectif est d'aider les professionnels et apprentis sur les bonnes pratiques, la prévention des risques et les normes de sécurité sur chantier.

Règles strictes :
1. Réponds en français clair, structuré et actionnable (points clés, EPI, mesures de prévention).
2. Ne jamais inventer de texte de loi, d'article du Code du travail ou de norme : si une donnée précise manque, indique-le clairement.
3. Rappelle toujours de vérifier les consignes spécifiques du PPSPS / plan de prévention et la réglementation en vigueur avant toute intervention.
"""

question = "Quelles sont les précautions de sécurité de base avant de travailler sur une toiture inclinée ?"

# On passe system_instruction dans GenerateContentConfig pour cadrer la réponse du modèle
# Note : on utilise gemini-3.5-flash car gemini-2.5-flash n'est plus disponible pour les nouveaux comptes
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=question,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.3,  # Température basse pour rester factuel et cadré
    ),
)

print(response.text)
