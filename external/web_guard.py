"""
Web Guard - Gestion du consentement utilisateur pour l'accès web
"""
import json
import os
from typing import Dict, Optional
from datetime import datetime

from config.settings import DATA_DIR


class WebGuard:
    """
    Gestionnaire de consentement pour l'utilisation du web.

    Responsabilités :
    - Vérifier si l'utilisateur autorise le web
    - Demander la permission
    - Logger les usages web
    - Respecter le choix de l'utilisateur
    """

    def __init__(self, user_profile=None):
        """
        Args:
            user_profile: Instance de UserPersonalization (optionnel)
        """
        self.user_profile = user_profile
        self.usage_log_file = os.path.join(DATA_DIR, "web_usage_log.json")
        self.usage_log = self._load_usage_log()

    def _load_usage_log(self) -> Dict:
        """Charge le log d'utilisation web"""
        try:
            if os.path.exists(self.usage_log_file):
                with open(self.usage_log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass

        return {
            "total_requests": 0,
            "requests_today": 0,
            "last_request_date": None,
            "history": []
        }

    def _save_usage_log(self):
        """Sauvegarde le log d'utilisation"""
        try:
            os.makedirs(os.path.dirname(self.usage_log_file), exist_ok=True)
            with open(self.usage_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde log web: {e}")

    # ========================================
    # VÉRIFICATION DU CONSENTEMENT
    # ========================================

    def can_use_web(self) -> bool:
        """
        Vérifie si le web peut être utilisé

        Returns:
            True si l'utilisateur a autorisé le web
        """
        if self.user_profile:
            return self.user_profile.web_enabled
        return False

    def is_web_enabled(self) -> bool:
        """Alias pour can_use_web()"""
        return self.can_use_web()

    def request_web_permission(self, reason: str = None) -> Dict:
        """
        Prépare une demande de permission pour le web

        Args:
            reason: Raison de la demande (optionnel)

        Returns:
            Dict avec les infos pour afficher la demande
        """
        return {
            "needs_permission": not self.can_use_web(),
            "reason": reason or "Cette fonctionnalité nécessite une recherche en ligne.",
            "message": "Souhaites-tu autoriser la recherche web pour enrichir les réponses ?",
            "benefits": [
                "Données actualisées et vérifiées",
                "Informations factuelles précises",
                "Enrichissement pédagogique"
            ],
            "privacy_note": "Les recherches sont anonymes et ne stockent pas de données personnelles."
        }

    def grant_permission(self):
        """Accorde la permission d'utiliser le web"""
        if self.user_profile:
            self.user_profile.web_enabled = True
            self._log_permission_change(True)

    def revoke_permission(self):
        """Révoque la permission d'utiliser le web"""
        if self.user_profile:
            self.user_profile.web_enabled = False
            self._log_permission_change(False)

    def toggle_permission(self) -> bool:
        """
        Bascule l'état de la permission

        Returns:
            Nouvel état (True = autorisé)
        """
        if self.user_profile:
            new_state = not self.user_profile.web_enabled
            self.user_profile.web_enabled = new_state
            self._log_permission_change(new_state)
            return new_state
        return False

    # ========================================
    # LOGGING DES USAGES
    # ========================================

    def log_web_usage(
        self,
        source: str,  # "perplexity", "anthropic", etc.
        query_type: str,  # "search", "enrich", "verify"
        subject: str = None,
        success: bool = True
    ):
        """
        Enregistre une utilisation du web

        Args:
            source: Source utilisée
            query_type: Type de requête
            subject: Matière concernée
            success: Si la requête a réussi
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Réinitialiser le compteur journalier si nouveau jour
        if self.usage_log.get("last_request_date") != today:
            self.usage_log["requests_today"] = 0
            self.usage_log["last_request_date"] = today

        # Incrémenter les compteurs
        self.usage_log["total_requests"] += 1
        self.usage_log["requests_today"] += 1

        # Ajouter à l'historique (limité)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "query_type": query_type,
            "subject": subject,
            "success": success
        }

        self.usage_log["history"].append(entry)

        # Limiter l'historique à 100 entrées
        if len(self.usage_log["history"]) > 100:
            self.usage_log["history"] = self.usage_log["history"][-100:]

        self._save_usage_log()

    def _log_permission_change(self, new_state: bool):
        """Log un changement de permission"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "permission_granted" if new_state else "permission_revoked"
        }

        if "permission_changes" not in self.usage_log:
            self.usage_log["permission_changes"] = []

        self.usage_log["permission_changes"].append(entry)
        self._save_usage_log()

    # ========================================
    # STATISTIQUES
    # ========================================

    def get_usage_stats(self) -> Dict:
        """Retourne les statistiques d'utilisation web"""
        return {
            "web_enabled": self.can_use_web(),
            "total_requests": self.usage_log.get("total_requests", 0),
            "requests_today": self.usage_log.get("requests_today", 0),
            "last_request_date": self.usage_log.get("last_request_date"),
            "history_count": len(self.usage_log.get("history", []))
        }

    def get_recent_usage(self, limit: int = 10) -> list:
        """Retourne les utilisations récentes"""
        history = self.usage_log.get("history", [])
        return history[-limit:] if history else []

    # ========================================
    # CONTRÔLE DE RATE
    # ========================================

    def check_rate_limit(self, max_daily: int = 50) -> bool:
        """
        Vérifie si la limite de requêtes n'est pas atteinte

        Args:
            max_daily: Limite de requêtes par jour

        Returns:
            True si on peut encore faire des requêtes
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Réinitialiser si nouveau jour
        if self.usage_log.get("last_request_date") != today:
            return True

        return self.usage_log.get("requests_today", 0) < max_daily

    def get_remaining_requests(self, max_daily: int = 50) -> int:
        """Retourne le nombre de requêtes restantes pour aujourd'hui"""
        today = datetime.now().strftime("%Y-%m-%d")

        if self.usage_log.get("last_request_date") != today:
            return max_daily

        return max(0, max_daily - self.usage_log.get("requests_today", 0))
