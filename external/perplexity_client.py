"""
Client API Perplexity - Recherche web factuelle avec consentement
"""
import requests
from typing import Dict, Optional, List

from config.settings import (
    PERPLEXITY_API_KEY,
    PERPLEXITY_API_URL,
    PERPLEXITY_MODEL,
    API_TIMEOUT,
    MAX_RETRIES
)


class PerplexityClient:
    """
    Client pour l'API Perplexity.

    Utilisé pour :
    - Recherches factuelles (dates, événements, formules)
    - Enrichissement pédagogique
    - Vérification d'informations

    IMPORTANT : N'utiliser QUE si l'utilisateur a autorisé le web
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or PERPLEXITY_API_KEY
        self.model = PERPLEXITY_MODEL
        self.api_url = PERPLEXITY_API_URL

    def is_available(self) -> bool:
        """Vérifie si le client est configuré"""
        return bool(self.api_key)

    def search(self, query: str, max_tokens: int = 1000) -> Optional[str]:
        """
        Effectue une recherche générale

        Args:
            query: Question ou recherche
            max_tokens: Limite de tokens

        Returns:
            Réponse textuelle ou None
        """
        if not self.is_available():
            print("⚠️ API Perplexity non configurée")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Tu es un assistant de recherche factuel. Réponds de manière concise et précise avec des faits vérifiables."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.2  # Faible pour des réponses factuelles
        }

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=API_TIMEOUT
                )

                if response.status_code == 200:
                    data = response.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content")
                    return None

                elif response.status_code == 429:
                    import time
                    time.sleep(2 ** attempt)
                    continue

                else:
                    print(f"⚠️ Erreur API Perplexity: {response.status_code}")
                    return None

            except requests.exceptions.Timeout:
                print(f"⚠️ Timeout Perplexity (tentative {attempt + 1}/{MAX_RETRIES})")
                continue

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Erreur réseau Perplexity: {e}")
                return None

        return None

    def enrich_topic(
        self,
        task: str,
        subject: str,
        topic: str = None
    ) -> Dict:
        """
        Enrichit un sujet avec des données factuelles

        Args:
            task: Description de la tâche
            subject: Matière
            topic: Thème spécifique

        Returns:
            Dict avec les données structurées
        """
        topic_str = f" sur {topic}" if topic else ""

        query = f"""Pour cette tâche scolaire de {subject}{topic_str}:
"{task}"

Fournis des informations factuelles précises au format JSON:
{{
    "definitions": [{{"term": "...", "definition": "..."}}],
    "dates": [{{"date": "...", "event": "..."}}],
    "formulas": [{{"name": "...", "formula": "...", "usage": "..."}}],
    "figures": [{{"name": "...", "role": "...", "period": "..."}}],
    "facts": ["fait 1", "fait 2"]
}}

Règles:
- Maximum 5 éléments par catégorie
- Informations vérifiables uniquement
- Adapté au niveau scolaire français"""

        response = self.search(query, max_tokens=1500)

        if response:
            try:
                import json
                # Chercher le JSON dans la réponse
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    data = json.loads(response[json_start:json_end])
                    data["success"] = True
                    return data
            except json.JSONDecodeError:
                pass

        return {
            "success": False,
            "definitions": [],
            "dates": [],
            "formulas": [],
            "figures": [],
            "facts": []
        }

    def get_factual_data(
        self,
        question: str,
        data_type: str = "general"
    ) -> Dict:
        """
        Récupère des données factuelles spécifiques

        Args:
            question: Question précise
            data_type: Type de données ("dates", "formulas", "definitions", "general")

        Returns:
            Dict avec les données
        """
        type_instructions = {
            "dates": "Fournis les dates importantes avec événements associés.",
            "formulas": "Fournis les formules avec leur nom et usage.",
            "definitions": "Fournis les définitions claires et concises.",
            "general": "Fournis les informations les plus pertinentes."
        }

        instruction = type_instructions.get(data_type, type_instructions["general"])

        query = f"""{instruction}

Question: {question}

Réponds au format JSON approprié. Sois précis et factuel."""

        response = self.search(query, max_tokens=1000)

        if response:
            try:
                import json
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    data = json.loads(response[json_start:json_end])
                    data["success"] = True
                    return data

                # Si pas de JSON, retourner le texte brut
                return {
                    "success": True,
                    "raw_response": response,
                    "data_type": data_type
                }
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "raw_response": response,
                    "data_type": data_type
                }

        return {"success": False}

    def verify_fact(self, statement: str) -> Dict:
        """
        Vérifie un fait

        Args:
            statement: Affirmation à vérifier

        Returns:
            Dict avec le résultat de vérification
        """
        query = f"""Vérifie cette affirmation et indique si elle est correcte:
"{statement}"

Réponds au format:
{{
    "is_correct": true/false,
    "explanation": "...",
    "correction": "..." (si incorrect)
}}"""

        response = self.search(query, max_tokens=500)

        if response:
            try:
                import json
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    return json.loads(response[json_start:json_end])
            except json.JSONDecodeError:
                pass

        return {
            "is_correct": None,
            "explanation": "Impossible de vérifier",
            "error": True
        }


class PerplexityFallback:
    """
    Fallback quand Perplexity n'est pas disponible.
    Utilise des données statiques ou locales.
    """

    @staticmethod
    def get_offline_data(subject: str, topic: str = None) -> Dict:
        """Retourne des données offline basiques"""
        # Importer les données des moteurs locaux
        from engines.base import SubjectEngineFactory

        engine = SubjectEngineFactory.get_engine(subject)

        if hasattr(engine, 'get_static_data'):
            return {
                "success": True,
                "source": "offline",
                **engine.get_static_data(topic or "", "premiere")
            }

        return {
            "success": False,
            "source": "offline",
            "message": "Données offline non disponibles pour ce sujet"
        }
