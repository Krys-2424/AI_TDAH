"""
Moteur pédagogique pour les sciences (physique, chimie, SVT)
"""
from typing import Dict, List

from .base import SubjectEngine


class ScienceEngine(SubjectEngine):
    """Moteur pédagogique pour les sciences (physique, chimie, SVT)"""

    @staticmethod
    def adapt_tasks(tasks: List[Dict], level: str, subject: str) -> List[Dict]:
        """Adapte pour les sciences : compréhension + application + expérimentation"""
        tier = SubjectEngine.get_level_tier(level)
        adapted = []

        # Phase 1: Compréhension concept
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "📖 Lire cours + surligner mots-clés", "lecture", "easy", 15
            ))
        elif tier == "lycee":
            adapted.append(SubjectEngine.create_task(
                "📖 Lire chapitre + noter définitions", "lecture", "medium", 20
            ))
        else:  # université
            adapted.append(SubjectEngine.create_task(
                "📚 Lire article scientifique + résumer", "lecture", "hard", 30
            ))

        # Phase 2: Schéma explicatif
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "✏️ Faire schéma simple légendé", "ecriture", "easy", 10
            ))
        else:
            adapted.append(SubjectEngine.create_task(
                "🖼️ Créer schéma détaillé + légendes", "ecriture", "medium", 15
            ))

        # Phase 3: Tâches originales
        for task in tasks:
            if "completed" not in task:
                task["completed"] = False
            adapted.append(task)

        # Phase 4: Exercices d'application
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "🎯 Faire 3 exercices simples", "exercices", "easy", 15
            ))
        elif tier == "lycee":
            adapted.append(SubjectEngine.create_task(
                "🔬 Résoudre 4 exercices types", "exercices", "medium", 25
            ))
        else:  # université
            adapted.append(SubjectEngine.create_task(
                "🧪 Résoudre problème complexe", "exercices", "hard", 30
            ))

        # Phase 5: Approfondissement lycée+
        if tier in ["lycee", "universite"]:
            adapted.append(SubjectEngine.create_task(
                "🔍 Analyser protocole expérimental", "recherche", "medium", 20
            ))

        # Phase 6: Approfondissement université
        if tier == "universite":
            adapted.append(SubjectEngine.create_task(
                "📊 Modélisation mathématique du phénomène", "ecriture", "hard", 25
            ))
            adapted.append(SubjectEngine.create_task(
                "🎭 Discussion critique résultats", "recherche", "hard", 20
            ))

        return adapted

    @staticmethod
    def get_static_data(task: str, level: str) -> Dict:
        """Retourne des données statiques enrichies pour les sciences"""
        task_lower = task.lower()
        result = {
            "definitions": [],
            "formulas": [],
            "methodology": [],
            "common_mistakes": []
        }

        # Lois de Newton
        if "newton" in task_lower or "force" in task_lower:
            result["definitions"] = [
                {"term": "Principe d'inertie (1ère loi)", "definition": "Un corps reste au repos ou en mouvement rectiligne uniforme si aucune force ne s'exerce"},
                {"term": "Principe fondamental (2ème loi)", "definition": "La somme des forces est égale à la masse fois l'accélération"},
                {"term": "Action-réaction (3ème loi)", "definition": "Si A exerce une force sur B, alors B exerce une force égale et opposée sur A"}
            ]
            result["formulas"] = [
                {"name": "Deuxième loi de Newton", "formula": "F = m × a", "usage": "Force (N) = masse (kg) × accélération (m/s²)"},
                {"name": "Poids", "formula": "P = m × g", "usage": "avec g ≈ 9,8 m/s² sur Terre"},
                {"name": "Vitesse", "formula": "v = d / t", "usage": "distance (m) divisée par temps (s)"}
            ]

        # Électricité
        elif "électricité" in task_lower or "circuit" in task_lower or "ohm" in task_lower:
            result["definitions"] = [
                {"term": "Tension électrique", "definition": "Différence de potentiel entre deux points, mesurée en Volts (V)"},
                {"term": "Intensité", "definition": "Débit de charges électriques, mesurée en Ampères (A)"},
                {"term": "Résistance", "definition": "Opposition au passage du courant, mesurée en Ohms (Ω)"}
            ]
            result["formulas"] = [
                {"name": "Loi d'Ohm", "formula": "U = R × I", "usage": "Tension = Résistance × Intensité"},
                {"name": "Puissance électrique", "formula": "P = U × I", "usage": "Puissance (W) = Tension × Intensité"},
            ]

        result["methodology"] = [
            "Lire le cours et identifier les concepts clés",
            "Faire un schéma ou dessin explicatif",
            "Appliquer les formules sur des exercices simples",
            "Vérifier les unités et l'ordre de grandeur"
        ]

        result["common_mistakes"] = [
            "Oublier les unités dans les calculs",
            "Confondre les formules",
            "Ne pas vérifier la cohérence du résultat"
        ]

        return result
