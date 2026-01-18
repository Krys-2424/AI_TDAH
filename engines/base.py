"""
Moteur pédagogique de base - Classe parent pour tous les moteurs par matière
"""
from typing import Dict, List

from config.tdah_rules import SCHOOL_LEVELS


class SubjectEngine:
    """Classe de base pour les moteurs pédagogiques par matière"""

    @staticmethod
    def get_level_tier(level: str) -> str:
        """Retourne le tier éducatif (college/lycee/universite)"""
        for tier, levels in SCHOOL_LEVELS.items():
            if level in levels:
                return tier
        return "lycee"

    @staticmethod
    def create_task(title: str, category: str, difficulty: str, time: int) -> Dict:
        """Helper pour créer une tâche avec tous les champs requis"""
        return {
            "title": title,
            "category": category,
            "difficulty": difficulty,
            "estimated_time": time,
            "completed": False
        }

    @staticmethod
    def adapt_tasks(tasks: List[Dict], level: str, subject: str) -> List[Dict]:
        """Adapte les tâches selon la matière et le niveau (à surcharger)"""
        return tasks

    @staticmethod
    def ensure_completed_field(tasks: List[Dict]) -> List[Dict]:
        """S'assure que toutes les tâches ont le champ 'completed'"""
        for task in tasks:
            if "completed" not in task:
                task["completed"] = False
        return tasks


class SubjectEngineFactory:
    """Factory pour obtenir le bon moteur selon la matière"""

    _engines = {}

    @classmethod
    def register_engine(cls, subject: str, engine_class):
        """Enregistre un moteur pour une matière"""
        cls._engines[subject] = engine_class

    @classmethod
    def get_engine(cls, subject: str) -> SubjectEngine:
        """Retourne le moteur approprié pour la matière"""
        # Import tardif pour éviter les imports circulaires
        if not cls._engines:
            from .maths import MathsEngine
            from .history import HistoryEngine
            from .science import ScienceEngine
            from .language import LanguageEngine

            cls._engines = {
                "maths": MathsEngine,
                "histoire": HistoryEngine,
                "géographie": HistoryEngine,
                "anglais": LanguageEngine,
                "espagnol": LanguageEngine,
                "allemand": LanguageEngine,
                "français": LanguageEngine,
                "physique": ScienceEngine,
                "chimie": ScienceEngine,
                "svt": ScienceEngine,
            }

        engine_class = cls._engines.get(subject, SubjectEngine)
        return engine_class()

    @staticmethod
    def ensure_completed_field(tasks: List[Dict]) -> List[Dict]:
        """S'assure que toutes les tâches ont le champ 'completed'"""
        for task in tasks:
            if "completed" not in task:
                task["completed"] = False
        return tasks
