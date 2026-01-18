"""
Client API Anthropic - Gère les appels à l'API Claude
"""
import requests
from typing import Dict, Optional, List

from config.settings import (
    ANTHROPIC_API_KEY,
    ANTHROPIC_ADMIN_API_KEY,
    ANTHROPIC_API_KEY_ID,
    ANTHROPIC_MODEL,
    ANTHROPIC_API_URL,
    API_TIMEOUT,
    MAX_RETRIES
)


class AnthropicClient:
    """Client pour l'API Anthropic (Claude)"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.model = ANTHROPIC_MODEL
        self.api_url = ANTHROPIC_API_URL

    def is_available(self) -> bool:
        """Vérifie si le client est configuré"""
        return bool(self.api_key)

    def send_message(
        self,
        prompt: str,
        max_tokens: int = 3000,
        temperature: float = 0.7,
        system_prompt: str = None
    ) -> Optional[str]:
        """
        Envoie un message à l'API Claude

        Args:
            prompt: Le message à envoyer
            max_tokens: Nombre maximum de tokens en réponse
            temperature: Créativité (0-1)
            system_prompt: Instructions système (optionnel)

        Returns:
            Le texte de réponse ou None en cas d'erreur
        """
        if not self.is_available():
            print("⚠️ API Anthropic non configurée")
            return None

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }

        messages = [{"role": "user", "content": prompt}]

        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        if system_prompt:
            payload["system"] = system_prompt

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
                    # Extraire le texte de la réponse
                    content = data.get("content", [])
                    for block in content:
                        if block.get("type") == "text":
                            return block.get("text")
                    return None

                elif response.status_code == 429:
                    # Rate limit - attendre et réessayer
                    import time
                    time.sleep(2 ** attempt)
                    continue

                else:
                    print(f"⚠️ Erreur API Anthropic: {response.status_code}")
                    print(f"Détails: {response.text[:200]}")
                    return None

            except requests.exceptions.Timeout:
                print(f"⚠️ Timeout API (tentative {attempt + 1}/{MAX_RETRIES})")
                continue

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Erreur réseau: {e}")
                return None

        return None

    def decompose_task(
        self,
        task: str,
        context: Dict,
        spiciness: int = 3,
        max_subtasks: int = 7
    ) -> Optional[List[str]]:
        """
        Décompose une tâche en sous-tâches

        Args:
            task: Description de la tâche
            context: Contexte analysé (sujet, niveau, etc.)
            spiciness: Niveau de détail (1-5)
            max_subtasks: Nombre maximum de sous-tâches

        Returns:
            Liste des sous-tâches ou None
        """
        # Utiliser le planner pour construire le prompt
        from core.planner import GoblinStyleDecomposer

        prompt = GoblinStyleDecomposer.build_spicy_prompt(
            task, context, spiciness, max_subtasks, 1.0
        )

        response = self.send_message(prompt, max_tokens=2000, temperature=0.5)

        if response:
            # Parser la réponse
            import re
            lines = [
                re.sub(r'^\d+\.\s*', '', line.strip())
                for line in response.split('\n')
                if re.match(r'^\d+\.', line.strip())
            ]
            return lines[:max_subtasks] if lines else None

        return None

    def get_enrichment(
        self,
        task: str,
        subject: str,
        level: str,
        elements_needed: List[str]
    ) -> Optional[Dict]:
        """
        Obtient des données d'enrichissement pédagogique

        Args:
            task: Description de la tâche
            subject: Matière
            level: Niveau scolaire
            elements_needed: Types d'éléments nécessaires

        Returns:
            Dict avec les données ou None
        """
        elements_str = ", ".join(elements_needed)

        prompt = f"""Tu es un expert pédagogique. Pour cette tâche scolaire, fournis des informations précises et factuelles.

TÂCHE: {task}
MATIÈRE: {subject}
NIVEAU: {level}
ÉLÉMENTS DEMANDÉS: {elements_str}

Réponds au format JSON structuré avec les clés demandées.
Ne mets que des informations vérifiables et adaptées au niveau."""

        response = self.send_message(prompt, max_tokens=2000, temperature=0.3)

        if response:
            try:
                import json
                # Chercher le JSON dans la réponse
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    return json.loads(response[json_start:json_end])
            except json.JSONDecodeError:
                pass

        return None


def get_api_key_info(api_key_id: str = None, admin_api_key: str = None) -> Optional[Dict]:
    """
    Récupère les informations d'une clé API Anthropic.

    Args:
        api_key_id: L'ID de la clé API à récupérer
        admin_api_key: La clé API admin pour l'authentification

    Returns:
        dict: Les informations de la clé API ou None en cas d'erreur
    """
    api_key_id = api_key_id or ANTHROPIC_API_KEY_ID
    admin_api_key = admin_api_key or ANTHROPIC_ADMIN_API_KEY

    if not api_key_id or not admin_api_key:
        return None

    url = f"https://api.anthropic.com/v1/organizations/api_keys/{api_key_id}"

    headers = {
        "X-Api-Key": admin_api_key
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des informations de la clé API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Détails: {e.response.text}")
        return None
