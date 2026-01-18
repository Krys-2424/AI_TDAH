"""
Moteur de feedback - Apprentissage sur la forme (spiciness, durée, difficulté)
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

from config.settings import FEEDBACK_FILE, DEFAULT_FEEDBACK, DATA_DIR


class FeedbackEngine:
    """
    Gère le feedback utilisateur sur la FORME des réponses :
    - Spiciness (niveau de détail)
    - Durée des tâches
    - Difficulté perçue
    - Satisfaction générale
    """

    def __init__(self, feedback_file: str = None):
        self.feedback_file = feedback_file or FEEDBACK_FILE
        self.feedback_data = self.load_feedback()

    def load_feedback(self) -> Dict:
        """Charge l'historique de feedback"""
        try:
            os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)

            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    return {**DEFAULT_FEEDBACK, **loaded}
        except Exception as e:
            print(f"⚠️ Erreur chargement feedback: {e}")

        return DEFAULT_FEEDBACK.copy()

    def save_feedback(self):
        """Sauvegarde l'historique de feedback"""
        try:
            os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde feedback: {e}")

    # ========================================
    # ENREGISTREMENT DU FEEDBACK
    # ========================================

    def record_spiciness_feedback(
        self,
        task_id: str,
        spiciness_used: int,
        feedback: str,  # "too_detailed", "just_right", "not_enough"
        subject: str = None
    ):
        """
        Enregistre le feedback sur le niveau de détail

        Args:
            task_id: ID de la tâche
            spiciness_used: Niveau utilisé (1-5)
            feedback: "too_detailed", "just_right", "not_enough"
            subject: Matière (optionnel)
        """
        entry = {
            "type": "spiciness",
            "task_id": task_id,
            "spiciness_used": spiciness_used,
            "feedback": feedback,
            "subject": subject,
            "timestamp": datetime.now().isoformat()
        }

        self.feedback_data["form_feedback"]["spiciness"].append(entry)
        self._limit_history()
        self.save_feedback()

    def record_duration_feedback(
        self,
        task_id: str,
        estimated_time: int,
        actual_time: int,
        feedback: str = None  # "too_long", "accurate", "too_short"
    ):
        """
        Enregistre le feedback sur la durée

        Args:
            task_id: ID de la tâche
            estimated_time: Temps estimé en minutes
            actual_time: Temps réel en minutes
            feedback: Feedback explicite ou auto-calculé
        """
        # Auto-détection si pas de feedback explicite
        if feedback is None:
            ratio = actual_time / estimated_time if estimated_time > 0 else 1
            if ratio > 1.3:
                feedback = "too_short"  # Estimation trop courte
            elif ratio < 0.7:
                feedback = "too_long"  # Estimation trop longue
            else:
                feedback = "accurate"

        entry = {
            "type": "duration",
            "task_id": task_id,
            "estimated_time": estimated_time,
            "actual_time": actual_time,
            "feedback": feedback,
            "efficiency": estimated_time / actual_time if actual_time > 0 else 1.0,
            "timestamp": datetime.now().isoformat()
        }

        self.feedback_data["form_feedback"]["duration"].append(entry)
        self._limit_history()
        self.save_feedback()

    def record_difficulty_feedback(
        self,
        task_id: str,
        estimated_difficulty: str,  # "easy", "medium", "hard"
        perceived_difficulty: str,
        subject: str = None
    ):
        """
        Enregistre le feedback sur la difficulté

        Args:
            task_id: ID de la tâche
            estimated_difficulty: Difficulté estimée
            perceived_difficulty: Difficulté ressentie
            subject: Matière (optionnel)
        """
        entry = {
            "type": "difficulty",
            "task_id": task_id,
            "estimated": estimated_difficulty,
            "perceived": perceived_difficulty,
            "subject": subject,
            "timestamp": datetime.now().isoformat()
        }

        self.feedback_data["form_feedback"]["difficulty"].append(entry)
        self._limit_history()
        self.save_feedback()

    def record_satisfaction_feedback(
        self,
        session_id: str,
        satisfaction: int,  # 1-5
        comment: str = None
    ):
        """
        Enregistre la satisfaction générale d'une session

        Args:
            session_id: ID de la session
            satisfaction: Score de 1 à 5
            comment: Commentaire optionnel
        """
        entry = {
            "type": "satisfaction",
            "session_id": session_id,
            "satisfaction": max(1, min(5, satisfaction)),
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }

        self.feedback_data["sessions"].append(entry)
        self._limit_history()
        self.save_feedback()

    # ========================================
    # ANALYSE DU FEEDBACK
    # ========================================

    def analyze_spiciness_trends(self, last_n: int = 20) -> Dict:
        """
        Analyse les tendances de feedback sur le spiciness

        Returns:
            Dict avec recommandations d'ajustement
        """
        spiciness_feedback = self.feedback_data["form_feedback"].get("spiciness", [])[-last_n:]

        if not spiciness_feedback:
            return {"adjustment": 0, "confidence": 0, "reason": "Pas assez de données"}

        too_detailed = sum(1 for f in spiciness_feedback if f["feedback"] == "too_detailed")
        not_enough = sum(1 for f in spiciness_feedback if f["feedback"] == "not_enough")
        just_right = sum(1 for f in spiciness_feedback if f["feedback"] == "just_right")

        total = len(spiciness_feedback)

        if too_detailed > not_enough and too_detailed > just_right:
            adjustment = -1
            reason = f"Trop détaillé {too_detailed}/{total} fois"
        elif not_enough > too_detailed and not_enough > just_right:
            adjustment = +1
            reason = f"Pas assez détaillé {not_enough}/{total} fois"
        else:
            adjustment = 0
            reason = f"Niveau adapté {just_right}/{total} fois"

        confidence = max(too_detailed, not_enough, just_right) / total if total > 0 else 0

        return {
            "adjustment": adjustment,
            "confidence": round(confidence, 2),
            "reason": reason,
            "stats": {
                "too_detailed": too_detailed,
                "just_right": just_right,
                "not_enough": not_enough
            }
        }

    def analyze_duration_accuracy(self, last_n: int = 20) -> Dict:
        """
        Analyse la précision des estimations de temps

        Returns:
            Dict avec statistiques et recommandations
        """
        duration_feedback = self.feedback_data["form_feedback"].get("duration", [])[-last_n:]

        if not duration_feedback:
            return {"avg_efficiency": 1.0, "needs_adjustment": False}

        efficiencies = [f.get("efficiency", 1.0) for f in duration_feedback]
        avg_efficiency = sum(efficiencies) / len(efficiencies)

        # Analyser les tendances
        too_short = sum(1 for f in duration_feedback if f["feedback"] == "too_short")
        too_long = sum(1 for f in duration_feedback if f["feedback"] == "too_long")

        needs_adjustment = abs(avg_efficiency - 1.0) > 0.2

        return {
            "avg_efficiency": round(avg_efficiency, 2),
            "needs_adjustment": needs_adjustment,
            "bias": "underestimate" if avg_efficiency < 0.8 else "overestimate" if avg_efficiency > 1.2 else "accurate",
            "stats": {
                "too_short": too_short,
                "too_long": too_long,
                "total": len(duration_feedback)
            }
        }

    def get_subject_difficulty_bias(self, subject: str, last_n: int = 10) -> float:
        """
        Calcule le biais de difficulté pour une matière

        Returns:
            float: Biais (-1 à +1), positif = perçu plus difficile
        """
        difficulty_map = {"easy": 1, "medium": 2, "hard": 3}

        all_difficulty = self.feedback_data["form_feedback"].get("difficulty", [])
        difficulty_feedback = [
            f for f in all_difficulty
            if f.get("subject") == subject
        ][-last_n:]

        if not difficulty_feedback:
            return 0.0

        biases = []
        for f in difficulty_feedback:
            estimated = difficulty_map.get(f["estimated"], 2)
            perceived = difficulty_map.get(f["perceived"], 2)
            biases.append((perceived - estimated) / 2)  # Normaliser entre -1 et +1

        return sum(biases) / len(biases) if biases else 0.0

    def get_average_satisfaction(self, last_n: int = 10) -> float:
        """Retourne la satisfaction moyenne récente"""
        satisfaction_feedback = [
            f for f in self.feedback_data.get("sessions", [])
            if f.get("type") == "satisfaction"
        ][-last_n:]

        if not satisfaction_feedback:
            return 3.0  # Neutre par défaut

        scores = [f["satisfaction"] for f in satisfaction_feedback]
        return sum(scores) / len(scores)

    # ========================================
    # SUGGESTIONS D'ADAPTATION
    # ========================================

    def get_adaptation_suggestions(self, user_profile) -> List[Dict]:
        """
        Génère des suggestions d'adaptation basées sur le feedback

        Args:
            user_profile: Instance de UserPersonalization

        Returns:
            Liste de suggestions avec priorité
        """
        suggestions = []

        # Analyse du spiciness
        spiciness_analysis = self.analyze_spiciness_trends()
        if spiciness_analysis["adjustment"] != 0 and spiciness_analysis["confidence"] > 0.5:
            current = user_profile.preferred_spiciness
            new = max(1, min(5, current + spiciness_analysis["adjustment"]))
            suggestions.append({
                "type": "spiciness",
                "priority": "high" if spiciness_analysis["confidence"] > 0.7 else "medium",
                "current": current,
                "suggested": new,
                "reason": spiciness_analysis["reason"]
            })

        # Analyse de la durée
        duration_analysis = self.analyze_duration_accuracy()
        if duration_analysis["needs_adjustment"]:
            suggestions.append({
                "type": "duration_estimation",
                "priority": "medium",
                "bias": duration_analysis["bias"],
                "avg_efficiency": duration_analysis["avg_efficiency"],
                "reason": f"Les estimations sont souvent {duration_analysis['bias']}"
            })

        # Satisfaction
        avg_satisfaction = self.get_average_satisfaction()
        if avg_satisfaction < 2.5:
            suggestions.append({
                "type": "general",
                "priority": "high",
                "reason": f"Satisfaction moyenne faible ({avg_satisfaction:.1f}/5)"
            })

        return sorted(suggestions, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["priority"], 2))

    def _limit_history(self, max_entries: int = 200):
        """Limite la taille de l'historique"""
        form_feedback = self.feedback_data.get("form_feedback", {})
        for key in ["spiciness", "duration", "difficulty"]:
            if key in form_feedback and len(form_feedback[key]) > max_entries:
                form_feedback[key] = form_feedback[key][-max_entries:]

        if len(self.feedback_data.get("sessions", [])) > max_entries:
            self.feedback_data["sessions"] = self.feedback_data["sessions"][-max_entries:]
