"""
Moteur pédagogique pour les mathématiques
"""
from typing import Dict, List

from .base import SubjectEngine


class MathsEngine(SubjectEngine):
    """Moteur pédagogique pour les mathématiques"""

    @staticmethod
    def adapt_tasks(tasks: List[Dict], level: str, subject: str) -> List[Dict]:
        """Adapte pour les maths : raisonnement logique + pratique"""
        tier = SubjectEngine.get_level_tier(level)
        adapted = []

        # Phase 1: Rappel des définitions (toujours)
        adapted.append(SubjectEngine.create_task(
            "📐 Revoir définitions et formules", "revision", "easy", 10
        ))

        # Phase 2: Exemples résolus
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "📖 Lire 2-3 exemples du cours", "lecture", "easy", 10
            ))
        else:
            adapted.append(SubjectEngine.create_task(
                "📖 Analyser exemples-types résolus", "lecture", "medium", 15
            ))

        # Phase 3: Tâches originales adaptées
        for task in tasks:
            if "completed" not in task:
                task["completed"] = False
            adapted.append(task)

        # Phase 4: Exercices progressifs
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "✏️ Faire 3 exercices simples", "exercices", "easy", 15
            ))
        elif tier == "lycee":
            adapted.append(SubjectEngine.create_task(
                "💪 Résoudre 5 exercices progressifs", "exercices", "medium", 25
            ))
        else:  # université
            adapted.append(SubjectEngine.create_task(
                "🧠 Résoudre problème type (méthode complète)", "exercices", "hard", 30
            ))

        # Phase 5: Vérification (toujours)
        adapted.append(SubjectEngine.create_task(
            "✅ Vérifier avec le corrigé", "revision", "easy", 10
        ))

        # Phase 6: Analyse d'erreurs (lycée+)
        if tier in ["lycee", "universite"]:
            adapted.append(SubjectEngine.create_task(
                "🔄 Refaire exercices ratés sans regarder", "exercices", "medium", 20
            ))

        # Phase 7: Approfondissement université
        if tier == "universite":
            adapted.append(SubjectEngine.create_task(
                "📝 Rédiger démonstration propre", "ecriture", "hard", 25
            ))
            adapted.append(SubjectEngine.create_task(
                "🤔 Chercher contre-exemple ou cas limite", "recherche", "hard", 20
            ))

        return adapted

    @staticmethod
    def get_static_data(task: str, level: str) -> Dict:
        """Retourne des données statiques enrichies pour les maths"""
        task_lower = task.lower()
        result = {
            "definitions": [],
            "formulas": [],
            "methodology": [],
            "common_mistakes": []
        }

        # Équations 2nd degré
        if "équation" in task_lower and ("2nd" in task_lower or "second" in task_lower or "discriminant" in task_lower):
            result["definitions"] = [
                {"term": "Équation du second degré", "definition": "Équation de la forme ax² + bx + c = 0 avec a ≠ 0"},
                {"term": "Discriminant", "definition": "Nombre Δ (delta) = b² - 4ac qui détermine le nombre de solutions"},
                {"term": "Racines", "definition": "Solutions de l'équation, calculées avec le discriminant"}
            ]
            result["formulas"] = [
                {"name": "Discriminant", "formula": "Δ = b² - 4ac", "usage": "Calculer en premier pour savoir combien de solutions"},
                {"name": "Racines (si Δ > 0)", "formula": "x₁ = (-b + √Δ) / 2a  et  x₂ = (-b - √Δ) / 2a", "usage": "Deux solutions distinctes"},
                {"name": "Racine double (si Δ = 0)", "formula": "x₀ = -b / 2a", "usage": "Une seule solution"},
            ]
            result["methodology"] = [
                "Identifier a, b et c dans l'équation",
                "Calculer le discriminant Δ = b² - 4ac",
                "Déterminer le nombre de solutions selon le signe de Δ",
                "Calculer les solutions si Δ ≥ 0"
            ]
            result["common_mistakes"] = [
                "Oublier le signe de a dans les formules",
                "Confondre -b et b dans les formules",
                "Oublier de vérifier que a ≠ 0"
            ]

        # Pythagore
        elif "pythagore" in task_lower or "triangle rectangle" in task_lower:
            result["definitions"] = [
                {"term": "Théorème de Pythagore", "definition": "Dans un triangle rectangle, le carré de l'hypoténuse est égal à la somme des carrés des deux autres côtés"},
                {"term": "Hypoténuse", "definition": "Le côté le plus long d'un triangle rectangle, opposé à l'angle droit"},
            ]
            result["formulas"] = [
                {"name": "Théorème de Pythagore", "formula": "a² + b² = c²", "usage": "c est l'hypoténuse, a et b les deux autres côtés"},
                {"name": "Calculer hypoténuse", "formula": "c = √(a² + b²)", "usage": "Quand on connaît les deux petits côtés"},
            ]

        # Dérivées
        elif "dérivée" in task_lower or "dériver" in task_lower:
            result["definitions"] = [
                {"term": "Dérivée", "definition": "Mesure la vitesse de variation d'une fonction en un point"},
                {"term": "Tangente", "definition": "Droite qui touche la courbe en un seul point, de pente f'(x₀)"},
            ]
            result["formulas"] = [
                {"name": "Dérivée de x^n", "formula": "(x^n)' = n × x^(n-1)", "usage": "Pour toute puissance de x"},
                {"name": "Dérivée de e^x", "formula": "(e^x)' = e^x", "usage": "La fonction exponentielle"},
                {"name": "Dérivée d'un produit", "formula": "(uv)' = u'v + uv'", "usage": "Produit de deux fonctions"}
            ]

        return result
