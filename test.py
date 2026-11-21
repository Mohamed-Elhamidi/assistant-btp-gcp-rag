import os
from dotenv import load_dotenv
from google import genai

# 1. Charge les variables depuis le fichier .env (ex: GEMINI_API_KEY)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("ClÃ© GEMINI_API_KEY introuvable dans l'environnement ou le .env")

# 2. Initialise le client Gemini (il lit automatiquement GEMINI_API_KEY si prÃ©sente)
client = genai.Client(api_key=api_key)

# 3. Envoie un prompt orientÃ© BTP au modÃ¨le
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=(
        "Explique en 3 points simples les principales rÃ¨gles de sÃ©curitÃ© "
        "pour le travail en hauteur sur un chantier BTP en France."
    ),
)

# 4. Affiche la rÃ©ponse textuelle dans le terminal
print(response.text)
