"""
Analyseur de tâches - Comprend et extrait le contexte des demandes utilisateur
"""
import re
from typing import Dict, List, Optional

from config.tdah_rules import SUBJECTS, TASK_TYPES, SCHOOL_LEVELS


class TaskAnalyzer:
    """Analyse la tâche pour extraire des informations contextuelles"""

    @staticmethod
    def analyze_context(task: str) -> Dict:
        """Analyse et extrait le contexte complet de la tâche"""
        task_lower = task.lower()
        context = {
            "subject": TaskAnalyzer.detect_subject(task_lower),
            "type": TaskAnalyzer.detect_task_type(task_lower),
            "level": TaskAnalyzer.detect_level(task_lower),
            "time_constraint": TaskAnalyzer.detect_time_constraint(task_lower),
            "materials": TaskAnalyzer.detect_materials(task_lower),
            "pages": TaskAnalyzer.extract_pages(task_lower),
            "exercises": TaskAnalyzer.extract_exercises(task_lower),
            "complexity": TaskAnalyzer.analyze_complexity(task)
        }
        return context

    @staticmethod
    def detect_subject(task: str) -> str:
        """Détecte la matière principale"""
        for subject, keywords in SUBJECTS.items():
            if any(keyword in task for keyword in keywords):
                return subject
        return "autre"

    @staticmethod
    def detect_task_type(task: str) -> str:
        """Détecte le type de tâche"""
        for task_type, keywords in TASK_TYPES.items():
            if any(keyword in task for keyword in keywords):
                return task_type
        return "autre"

    @staticmethod
    def detect_level(task: str) -> str:
        """Détecte le niveau scolaire précis (collège → L3)"""
        task_lower = task.lower()

        # Détection précise du niveau
        level_patterns = {
            "6eme": ["6ème", "6eme", "sixième"],
            "5eme": ["5ème", "5eme", "cinquième"],
            "4eme": ["4ème", "4eme", "quatrième"],
            "3eme": ["3ème", "3eme", "troisième"],
            "seconde": ["seconde", "2nde"],
            "premiere": ["première", "1ère", "1ere"],
            "terminale": ["terminale", "term", "bac"],
            "L1": ["l1", "licence 1", "première année"],
            "L2": ["l2", "licence 2", "deuxième année"],
            "L3": ["l3", "licence 3", "troisième année"]
        }

        for level, patterns in level_patterns.items():
            if any(pattern in task_lower for pattern in patterns):
                return level

        # Détection par catégorie générale
        if "collège" in task_lower or "college" in task_lower:
            return "4eme"
        elif "lycée" in task_lower or "lycee" in task_lower:
            return "premiere"
        elif "université" in task_lower or "universite" in task_lower or "fac" in task_lower:
            return "L2"

        return "premiere"  # Défaut

    @staticmethod
    def detect_time_constraint(task: str) -> Optional[str]:
        """Détecte les contraintes de temps"""
        if any(word in task for word in ["demain", "aujourd'hui", "urgent"]):
            return "urgent"
        elif any(word in task for word in ["semaine", "lundi", "mardi", "mercredi", "jeudi", "vendredi"]):
            return "cette_semaine"
        elif any(word in task for word in ["mois", "prochain"]):
            return "long_terme"
        return None

    @staticmethod
    def detect_materials(task: str) -> List[str]:
        """Détecte les matériaux mentionnés"""
        materials = []
        material_keywords = {
            "livre": ["livre", "manuel"],
            "cours": ["cours", "leçon"],
            "exercices": ["exercice"],
            "corrigé": ["corrigé", "correction"]
        }

        for material, keywords in material_keywords.items():
            if any(keyword in task for keyword in keywords):
                materials.append(material)
        return materials

    @staticmethod
    def extract_pages(task: str) -> Optional[Dict]:
        """Extrait les numéros de pages mentionnés"""
        patterns = [
            r'pages?\s*(\d+)\s*(?:à|-)?\s*(\d+)?',
            r'p\.\s*(\d+)\s*(?:à|-)?\s*(\d+)?'
        ]

        for pattern in patterns:
            match = re.search(pattern, task.lower())
            if match:
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else start
                return {"start": start, "end": end}
        return None

    @staticmethod
    def extract_exercises(task: str) -> Optional[List[int]]:
        """Extrait les numéros d'exercices"""
        patterns = [
            r'exercices?\s*(\d+)\s*(?:à|-)?\s*(\d+)?',
            r'ex\s*(\d+)\s*(?:à|-)?\s*(\d+)?'
        ]

        for pattern in patterns:
            match = re.search(pattern, task.lower())
            if match:
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else start
                return list(range(start, end + 1))
        return None

    @staticmethod
    def analyze_complexity(task_desc: str) -> Dict:
        """Analyse la complexité réelle d'une tâche"""
        complexity_score = 0

        # Mots indiquant de la complexité
        complex_words = ["analyser", "créer", "développer", "construire", "comparer",
                        "synthétiser", "argumenter", "démontrer", "concevoir"]
        simple_words = ["lire", "copier", "noter", "surligner", "recopier", "relire"]

        task_lower = task_desc.lower()

        # Comptage
        complexity_score += sum(2 for word in complex_words if word in task_lower)
        complexity_score -= sum(1 for word in simple_words if word in task_lower)

        # Longueur de la description (plus c'est long, plus c'est complexe)
        if len(task_desc) > 100:
            complexity_score += 2
        elif len(task_desc) > 50:
            complexity_score += 1

        # Présence de chiffres/quantités
        if any(char.isdigit() for char in task_desc):
            complexity_score += 1

        return {
            "score": complexity_score,
            "level": "hard" if complexity_score >= 4 else "medium" if complexity_score >= 1 else "easy",
            "estimated_focus_time": min(30, 15 + complexity_score * 3)
        }

    @staticmethod
    def get_level_tier(level: str) -> str:
        """Retourne le tier éducatif (college/lycee/universite)"""
        for tier, levels in SCHOOL_LEVELS.items():
            if level in levels:
                return tier
        return "lycee"

    @staticmethod
    def requires_factual_data(task: str, subject: str) -> bool:
        """Détermine si la tâche nécessite des données factuelles précises"""
        task_lower = task.lower()

        # Mots-clés indiquant besoin de données factuelles
        factual_keywords = [
            "date", "année", "quand", "qui", "événement",
            "formule", "théorème", "définition", "loi",
            "personnage", "auteur", "découverte"
        ]

        # Matières nécessitant souvent des données factuelles
        factual_subjects = ["histoire", "physique", "chimie", "svt", "géographie"]

        has_factual_keywords = any(kw in task_lower for kw in factual_keywords)
        is_factual_subject = subject in factual_subjects

        return has_factual_keywords or is_factual_subject
