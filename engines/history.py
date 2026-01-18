"""
Moteur pédagogique pour l'histoire et la géographie
"""
from typing import Dict, List

from .base import SubjectEngine


class HistoryEngine(SubjectEngine):
    """Moteur pédagogique pour l'histoire"""

    @staticmethod
    def adapt_tasks(tasks: List[Dict], level: str, subject: str) -> List[Dict]:
        """Adapte pour l'histoire : compréhension + analyse critique"""
        tier = SubjectEngine.get_level_tier(level)
        adapted = []

        # Phase 1: Repérage chronologique (toujours)
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "📅 Créer frise chronologique simple", "ecriture", "easy", 10
            ))
        else:
            adapted.append(SubjectEngine.create_task(
                "📅 Situer dans contexte historique large", "revision", "medium", 15
            ))

        # Phase 2: Tâches originales
        for task in tasks:
            if "completed" not in task:
                task["completed"] = False
            adapted.append(task)

        # Phase 3: Analyse de documents
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "🖼️ Lire 1 document source + 3 questions", "lecture", "easy", 15
            ))
        elif tier == "lycee":
            adapted.append(SubjectEngine.create_task(
                "📜 Analyser 2-3 documents (nature, auteur, contexte)", "lecture", "medium", 20
            ))
        else:  # université
            adapted.append(SubjectEngine.create_task(
                "📚 Lire article scientifique (10 pages max)", "lecture", "hard", 30
            ))

        # Phase 4: Synthèse
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "📝 Écrire résumé en 10 lignes", "ecriture", "easy", 15
            ))
        elif tier == "lycee":
            adapted.append(SubjectEngine.create_task(
                "✏️ Rédiger plan détaillé avec arguments", "ecriture", "medium", 20
            ))

        # Phase 5: Approfondissement université
        if tier == "universite":
            adapted.append(SubjectEngine.create_task(
                "🔍 Analyse historiographique (écoles de pensée)", "recherche", "hard", 25
            ))
            adapted.append(SubjectEngine.create_task(
                "🎭 Construire problématique + plan thématique", "ecriture", "hard", 25
            ))

        return adapted

    @staticmethod
    def get_static_data(task: str, level: str) -> Dict:
        """Retourne des données statiques enrichies pour l'histoire"""
        task_lower = task.lower()
        result = {
            "definitions": [],
            "dates": [],
            "figures": [],
            "methodology": [],
            "common_mistakes": []
        }

        # Révolution Française
        if "révolution" in task_lower and "français" in task_lower:
            result["dates"] = [
                {"date": "14 juillet 1789", "event": "Prise de la Bastille, symbole de la Révolution"},
                {"date": "26 août 1789", "event": "Déclaration des Droits de l'Homme et du Citoyen"},
                {"date": "21 septembre 1792", "event": "Proclamation de la Première République"},
                {"date": "21 janvier 1793", "event": "Exécution de Louis XVI"},
                {"date": "27 juillet 1794", "event": "Chute de Robespierre (9 Thermidor)"},
                {"date": "9 novembre 1799", "event": "Coup d'État de Napoléon Bonaparte (18 Brumaire)"}
            ]
            result["figures"] = [
                {"name": "Louis XVI", "role": "Roi de France renversé et exécuté", "period": "1774-1793"},
                {"name": "Maximilien de Robespierre", "role": "Leader jacobin, période de la Terreur", "period": "1793-1794"},
                {"name": "Georges Danton", "role": "Révolutionnaire modéré, guillotiné", "period": "1793-1794"},
                {"name": "Napoléon Bonaparte", "role": "Général qui prend le pouvoir", "period": "1799-1815"}
            ]
            result["definitions"] = [
                {"term": "Tiers État", "definition": "Le peuple (98% population) : paysans, artisans, bourgeois"},
                {"term": "Sans-culottes", "definition": "Révolutionnaires radicaux du peuple parisien"},
                {"term": "Jacobins", "definition": "Groupe politique révolutionnaire radical (Robespierre)"}
            ]

        # Première Guerre Mondiale
        elif "guerre" in task_lower and ("14" in task_lower or "1914" in task_lower or "mondiale" in task_lower):
            result["dates"] = [
                {"date": "28 juin 1914", "event": "Assassinat de l'archiduc François-Ferdinand à Sarajevo"},
                {"date": "Août 1914", "event": "Début de la guerre, jeu des alliances"},
                {"date": "1916", "event": "Bataille de Verdun (300 000 morts)"},
                {"date": "1917", "event": "Entrée en guerre des États-Unis"},
                {"date": "11 novembre 1918", "event": "Armistice, fin de la guerre"},
                {"date": "28 juin 1919", "event": "Traité de Versailles"}
            ]
            result["figures"] = [
                {"name": "Georges Clemenceau", "role": "Président du Conseil français", "period": "1917-1920"},
                {"name": "Guillaume II", "role": "Kaiser allemand", "period": "1888-1918"},
                {"name": "Philippe Pétain", "role": "Général français, vainqueur de Verdun", "period": "1916"}
            ]

        result["methodology"] = [
            "Créer une frise chronologique",
            "Identifier les causes et conséquences",
            "Analyser les documents sources",
            "Contextualiser les événements"
        ]

        result["common_mistakes"] = [
            "Confondre les dates",
            "Oublier le contexte",
            "Réciter sans analyser"
        ]

        return result
