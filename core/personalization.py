"""
Système de personnalisation utilisateur - Profil dynamique adaptatif
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

from config.settings import USER_PROFILE_FILE, DEFAULT_USER_PROFILE, DATA_DIR


class UserPersonalization:
    """Gère le profil utilisateur et ses préférences adaptatives"""

    def __init__(self, profile_file: str = None):
        self.profile_file = profile_file or USER_PROFILE_FILE
        self.profile = self.load_profile()

    def load_profile(self) -> Dict:
        """Charge le profil utilisateur depuis le fichier"""
        try:
            # Créer le dossier data si nécessaire
            os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)

            if os.path.exists(self.profile_file):
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Fusionner avec les valeurs par défaut
                    profile = {**DEFAULT_USER_PROFILE, **loaded}
                    return profile
        except Exception as e:
            print(f"⚠️ Erreur chargement profil: {e}")

        return DEFAULT_USER_PROFILE.copy()

    def save_profile(self):
        """Sauvegarde le profil utilisateur"""
        try:
            os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde profil: {e}")

    # ========================================
    # ACCESSEURS / MUTATEURS
    # ========================================

    @property
    def preferred_spiciness(self) -> int:
        """Niveau de spiciness préféré (1-5)"""
        return self.profile.get("preferred_spiciness", 3)

    @preferred_spiciness.setter
    def preferred_spiciness(self, value: int):
        self.profile["preferred_spiciness"] = max(1, min(5, value))
        self.save_profile()

    @property
    def focus_duration(self) -> int:
        """Durée de concentration optimale en minutes"""
        return self.profile.get("focus_duration", 20)

    @focus_duration.setter
    def focus_duration(self, value: int):
        self.profile["focus_duration"] = max(5, min(60, value))
        self.save_profile()

    @property
    def fatigue_sensitivity(self) -> float:
        """Sensibilité à la fatigue (0.0 à 1.0)"""
        return self.profile.get("fatigue_sensitivity", 0.5)

    @fatigue_sensitivity.setter
    def fatigue_sensitivity(self, value: float):
        self.profile["fatigue_sensitivity"] = max(0.0, min(1.0, value))
        self.save_profile()

    @property
    def web_enabled(self) -> bool:
        """Autorisation d'utiliser le web pour enrichir les réponses"""
        return self.profile.get("web_enabled", False)

    @web_enabled.setter
    def web_enabled(self, value: bool):
        self.profile["web_enabled"] = value
        self.save_profile()

    @property
    def total_tasks_completed(self) -> int:
        """Nombre total de tâches complétées"""
        return self.profile.get("total_tasks_completed", 0)

    @property
    def streak_days(self) -> int:
        """Nombre de jours consécutifs de travail"""
        return self.profile.get("streak_days", 0)

    # ========================================
    # MÉTHODES DE PERSONNALISATION
    # ========================================

    def get_difficulty_bias(self, subject: str) -> float:
        """
        Retourne le biais de difficulté pour une matière

        Args:
            subject: Nom de la matière

        Returns:
            float: Biais (-1.0 à +1.0), positif = plus difficile que la moyenne
        """
        biases = self.profile.get("difficulty_bias", {})
        return biases.get(subject, 0)

    def set_difficulty_bias(self, subject: str, bias: float):
        """Définit le biais de difficulté pour une matière"""
        if "difficulty_bias" not in self.profile:
            self.profile["difficulty_bias"] = {}
        self.profile["difficulty_bias"][subject] = max(-1.0, min(1.0, bias))
        self.save_profile()

    def adjust_difficulty_bias(self, subject: str, adjustment: float):
        """Ajuste progressivement le biais de difficulté"""
        current = self.get_difficulty_bias(subject)
        new_bias = current + adjustment * 0.1  # Ajustement progressif
        self.set_difficulty_bias(subject, new_bias)

    def get_preferred_hours(self) -> Dict[str, int]:
        """Retourne les heures préférées avec leur fréquence"""
        return self.profile.get("preferred_hours", {})

    def record_activity_hour(self, hour: int):
        """Enregistre une activité à une heure donnée"""
        hours = self.profile.get("preferred_hours", {})
        hour_str = str(hour)
        hours[hour_str] = hours.get(hour_str, 0) + 1
        self.profile["preferred_hours"] = hours
        self.save_profile()

    def get_best_hours(self, top_n: int = 3) -> List[int]:
        """Retourne les heures les plus productives"""
        hours = self.get_preferred_hours()
        if not hours:
            return [9, 14, 16]  # Heures par défaut

        sorted_hours = sorted(hours.items(), key=lambda x: x[1], reverse=True)
        return [int(h) for h, _ in sorted_hours[:top_n]]

    def increment_tasks_completed(self):
        """Incrémente le compteur de tâches complétées"""
        self.profile["total_tasks_completed"] = self.total_tasks_completed + 1
        self.save_profile()

    def update_last_session(self):
        """Met à jour la date de dernière session"""
        self.profile["last_session"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_profile()

    def update_streak(self):
        """Met à jour la série de jours consécutifs"""
        last_session = self.profile.get("last_session")
        today = datetime.now().strftime("%Y-%m-%d")

        if last_session:
            try:
                last_date = datetime.strptime(last_session.split()[0], "%Y-%m-%d").strftime("%Y-%m-%d")
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

                if last_date == today:
                    pass  # Déjà travaillé aujourd'hui
                elif last_date == yesterday:
                    self.profile["streak_days"] = self.streak_days + 1
                else:
                    self.profile["streak_days"] = 1  # Série cassée
            except ValueError:
                self.profile["streak_days"] = 1
        else:
            self.profile["streak_days"] = 1

        self.save_profile()

    def get_subject_preference(self, subject: str) -> Dict:
        """Retourne les préférences pour une matière"""
        prefs = self.profile.get("subject_preferences", {})
        return prefs.get(subject, {
            "times_worked": 0,
            "avg_efficiency": 1.0,
            "preferred_spiciness": self.preferred_spiciness
        })

    def update_subject_preference(self, subject: str, efficiency: float):
        """Met à jour les préférences pour une matière après travail"""
        prefs = self.profile.get("subject_preferences", {})

        if subject not in prefs:
            prefs[subject] = {
                "times_worked": 0,
                "avg_efficiency": 1.0,
                "preferred_spiciness": self.preferred_spiciness
            }

        # Mise à jour moyenne glissante
        old_count = prefs[subject]["times_worked"]
        old_avg = prefs[subject]["avg_efficiency"]

        prefs[subject]["times_worked"] = old_count + 1
        prefs[subject]["avg_efficiency"] = (old_avg * old_count + efficiency) / (old_count + 1)

        self.profile["subject_preferences"] = prefs
        self.save_profile()

    # ========================================
    # SUGGESTIONS INTELLIGENTES
    # ========================================

    def suggest_spiciness_for_context(self, subject: str, hour: int, fatigue_detected: bool) -> int:
        """
        Suggère un niveau de spiciness adapté au contexte

        Args:
            subject: Matière en cours
            hour: Heure actuelle
            fatigue_detected: Si fatigue est détectée
        """
        base = self.preferred_spiciness

        # Ajustements
        if fatigue_detected:
            base = max(1, base - 1)  # Moins détaillé si fatigué

        # Matin tôt ou soir tard -> simplifier
        if hour < 8 or hour > 21:
            base = max(1, base - 1)

        # Matière difficile pour l'utilisateur -> plus détaillé
        bias = self.get_difficulty_bias(subject)
        if bias > 0.3:
            base = min(5, base + 1)

        return base

    def suggest_break_activity(self, session_duration: int) -> str:
        """Suggère une activité de pause selon la durée de travail"""
        if session_duration < 20:
            return "🧊 Boire de l'eau + étirements (2 min)"
        elif session_duration < 40:
            return "🚶 Marcher 5 min + respiration"
        else:
            return "🧘 Pause complète : marche + collation + air frais (10 min)"

    def get_productivity_summary(self) -> Dict:
        """Retourne un résumé de la productivité"""
        return {
            "total_completed": self.total_tasks_completed,
            "streak_days": self.streak_days,
            "preferred_spiciness": self.preferred_spiciness,
            "focus_duration": self.focus_duration,
            "best_hours": self.get_best_hours(3),
            "web_enabled": self.web_enabled
        }

    # ========================================
    # PRÉDICTIONS PERSONNALISÉES
    # ========================================

    def personalized_estimate(
        self,
        category: str,
        difficulty: str,
        base_time: int
    ) -> int:
        """
        Estime le temps personnalisé basé sur l'historique utilisateur

        Args:
            category: Catégorie de la tâche
            difficulty: Difficulté de la tâche (easy, medium, hard)
            base_time: Temps de base estimé en minutes

        Returns:
            int: Temps estimé personnalisé en minutes
        """
        # Récupérer l'historique des durées pour cette catégorie
        duration_history = self.profile.get("duration_history", {})
        category_history = duration_history.get(category, [])

        # Si on a assez d'historique (au moins 3 entrées), utiliser la moyenne
        if len(category_history) >= 3:
            avg_time = sum(category_history) / len(category_history)
            # Pondération 70% historique, 30% estimation de base
            estimated = int(avg_time * 0.7 + base_time * 0.3)
        else:
            estimated = base_time

        # Ajuster selon le biais de difficulté utilisateur
        difficulty_multipliers = {"easy": 0.8, "medium": 1.0, "hard": 1.3}
        difficulty_mult = difficulty_multipliers.get(difficulty, 1.0)

        # Ajuster selon la sensibilité à la fatigue (ajoute du temps si fatigué)
        fatigue_mult = 1.0 + (self.fatigue_sensitivity * 0.2)

        # Calcul final
        final_estimate = int(estimated * difficulty_mult * fatigue_mult)

        # Borner entre 5 et 45 minutes
        return max(5, min(45, final_estimate))

    def record_task_duration(self, category: str, actual_duration: int):
        """
        Enregistre la durée réelle d'une tâche pour améliorer les prédictions

        Args:
            category: Catégorie de la tâche
            actual_duration: Durée réelle en minutes
        """
        if "duration_history" not in self.profile:
            self.profile["duration_history"] = {}

        if category not in self.profile["duration_history"]:
            self.profile["duration_history"][category] = []

        # Garder les 20 dernières entrées par catégorie
        history = self.profile["duration_history"][category]
        history.append(actual_duration)
        if len(history) > 20:
            history = history[-20:]

        self.profile["duration_history"][category] = history
        self.save_profile()


# Import pour update_streak
from datetime import timedelta
