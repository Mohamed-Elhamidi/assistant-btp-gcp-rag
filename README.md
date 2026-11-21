# Assistant BTP GCP RAG

Assistant intelligent pour le secteur du BTP (Bâtiment et Travaux Publics) combinant Google Cloud Platform (GCP), l'API Gemini et une architecture RAG (Retrieval-Augmented Generation).

## Structure du projet

- `test.py` : Script de test de connexion à l'API Gemini.
- `.env.example` : Modèle pour les variables d'environnement.
- `.gitignore` : Exclusions Git pour protéger les secrets et l'environnement virtuel.

## Installation et configuration

1. **Créer et activer l'environnement virtuel (`.venv`) :**

   * **Créer l'environnement :**
     ```bash
     python -m venv .venv
     ```

   * **Activer sous Windows (PowerShell) :**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
     *(Si PowerShell bloque l'exécution de scripts avec une erreur de sécurité, autorisez-le une seule fois avec :)*  
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

   * **Activer sous Windows (Invite de commandes CMD) :**
     ```cmd
     .\.venv\Scripts\activate.bat
     ```

   * **Activer sous macOS / Linux :**
     ```bash
     source .venv/bin/activate
     ```

   *(Lorsque l'environnement est actif, le préfixe `(.venv)` apparaît au début de la ligne de votre terminal).*

2. **Installer les dépendances :**
   ```bash
   pip install google-genai python-dotenv
   ```

3. **Configurer les variables d'environnement :**
   - Dupliquer `.env.example` en `.env`
   - Renseigner votre clé `GEMINI_API_KEY`

4. **Tester la connexion :**
   ```bash
   python test.py
   ```
