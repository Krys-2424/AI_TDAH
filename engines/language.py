"""
Moteur pédagogique pour les langues (français, anglais, espagnol, allemand)
"""
from typing import Dict, List

from .base import SubjectEngine


class LanguageEngine(SubjectEngine):
    """Moteur pédagogique pour les langues"""

    @staticmethod
    def adapt_tasks(tasks: List[Dict], level: str, subject: str) -> List[Dict]:
        """Adapte pour les langues : répétition + production + immersion"""
        tier = SubjectEngine.get_level_tier(level)
        adapted = []

        # Phase 1: Vocabulaire (toujours)
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "📚 Apprendre 10 mots + exemple", "revision", "easy", 10
            ))
        elif tier == "lycee":
            adapted.append(SubjectEngine.create_task(
                "📚 Apprendre 15 mots + phrases contextuelles", "revision", "medium", 15
            ))
        else:  # université
            adapted.append(SubjectEngine.create_task(
                "🎯 Maîtriser 20 mots spécialisés + nuances", "revision", "hard", 15
            ))

        # Phase 2: Compréhension orale
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "🎧 Écouter dialogue simple 2x", "lecture", "easy", 10
            ))
        else:
            adapted.append(SubjectEngine.create_task(
                "🎧 Écouter audio authentique + noter idées", "lecture", "medium", 15
            ))

        # Phase 3: Tâches originales
        for task in tasks:
            if "completed" not in task:
                task["completed"] = False
            adapted.append(task)

        # Phase 4: Expression écrite
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "✏️ Écrire 5 phrases simples", "ecriture", "easy", 15
            ))
        elif tier == "lycee":
            adapted.append(SubjectEngine.create_task(
                "📝 Rédiger paragraphe argumenté (150 mots)", "ecriture", "medium", 20
            ))
        else:  # université
            adapted.append(SubjectEngine.create_task(
                "📄 Rédiger essai structuré (300 mots)", "ecriture", "hard", 30
            ))

        # Phase 5: Expression orale
        if tier == "college":
            adapted.append(SubjectEngine.create_task(
                "🗣️ Répéter 10 phrases à voix haute", "revision", "easy", 10
            ))
        elif tier == "lycee":
            adapted.append(SubjectEngine.create_task(
                "💬 Préparer présentation orale 2 min", "revision", "medium", 15
            ))
        else:  # université
            adapted.append(SubjectEngine.create_task(
                "🎤 Préparer débat argumenté (3 arguments)", "revision", "hard", 20
            ))

        # Phase 6: Approfondissement université
        if tier == "universite":
            adapted.append(SubjectEngine.create_task(
                "📖 Analyse stylistique texte littéraire", "lecture", "hard", 25
            ))

        return adapted

    @staticmethod
    def get_static_data(task: str, level: str) -> Dict:
        """Retourne des données statiques enrichies pour les langues"""
        result = {
            "definitions": [],
            "methodology": [],
            "common_mistakes": []
        }

        result["methodology"] = [
            "Apprendre le vocabulaire avec des exemples en contexte",
            "Pratiquer l'écoute active (podcasts, vidéos)",
            "Écrire régulièrement (journal, résumés)",
            "Parler à voix haute pour améliorer la prononciation",
            "Réviser avec des flashcards"
        ]

        result["common_mistakes"] = [
            "Traduire mot à mot depuis le français",
            "Négliger la prononciation",
            "Ne pas réviser régulièrement le vocabulaire",
            "Avoir peur de faire des erreurs à l'oral"
        ]

        return result
