"""
Feedback pédagogique - Analyse des critiques sur le CONTENU
Transforme "il manque les dates" en données structurées
"""
import json
import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from config.settings import DATA_DIR


class PedagogicalFeedback:
    """
    Analyse les retours utilisateur sur le CONTENU pédagogique.
    Identifie ce qui manque et enrichit la mémoire de savoir.

    Exemples de feedback analysés:
    - "Il manque les dates"
    - "Pas assez de formules"
    - "J'aurais aimé avoir les personnages importants"
    - "Les définitions ne sont pas claires"
    """

    # Mapping des mots-clés vers les types d'éléments manquants
    ELEMENT_PATTERNS = {
        "dates": [
            r"date[s]?", r"année[s]?", r"quand", r"chronologi[eq]",
            r"période[s]?", r"époque[s]?", r"siècle[s]?"
        ],
        "figures": [
            r"personnage[s]?", r"auteur[s]?", r"scientifique[s]?",
            r"qui", r"nom[s]?", r"personne[s]?", r"historien[s]?"
        ],
        "definitions": [
            r"définition[s]?", r"terme[s]?", r"vocabulaire",
            r"mot[s]?-clé[s]?", r"concept[s]?", r"notion[s]?"
        ],
        "formulas": [
            r"formule[s]?", r"équation[s]?", r"calcul[s]?",
            r"théorème[s]?", r"loi[s]?", r"propriété[s]?"
        ],
        "examples": [
            r"exemple[s]?", r"illustration[s]?", r"cas",
            r"application[s]?", r"exercice[s]? résolu[s]?"
        ],
        "methodology": [
            r"méthode[s]?", r"méthodologi[eq]", r"étape[s]?",
            r"comment", r"procédure[s]?", r"démarche[s]?"
        ],
        "context": [
            r"contexte", r"cause[s]?", r"conséquence[s]?",
            r"pourquoi", r"raison[s]?", r"origine[s]?"
        ],
        "summary": [
            r"résumé", r"synthèse", r"récapitulatif",
            r"l'essentiel", r"points? clé[s]?"
        ]
    }

    # Mots indiquant un manque
    MISSING_INDICATORS = [
        r"manque", r"pas assez", r"insuffisant", r"absent",
        r"aurais aimé", r"aurais voulu", r"il faudrait",
        r"besoin de", r"ajouter", r"plus de", r"où sont"
    ]

    # Mots indiquant un problème de qualité
    QUALITY_INDICATORS = [
        r"pas clair", r"confus", r"incompréhensible", r"compliqué",
        r"mal expliqué", r"difficile à comprendre", r"flou"
    ]

    def __init__(self, knowledge_memory=None):
        """
        Args:
            knowledge_memory: Instance de KnowledgeMemory pour mise à jour
        """
        self.knowledge_memory = knowledge_memory
        self.feedback_history = []

    def parse_feedback_text(self, feedback_text: str, subject: str = None, topic: str = None) -> Dict:
        """
        Analyse un texte de feedback et extrait les éléments structurés

        Args:
            feedback_text: Texte libre de l'utilisateur
            subject: Matière concernée (optionnel)
            topic: Thème spécifique (optionnel)

        Returns:
            Dict avec les éléments identifiés
        """
        feedback_lower = feedback_text.lower()

        result = {
            "original_text": feedback_text,
            "subject": subject,
            "topic": topic,
            "missing_elements": [],
            "quality_issues": [],
            "sentiment": self._detect_sentiment(feedback_lower),
            "timestamp": datetime.now().isoformat()
        }

        # Détecter les éléments manquants
        is_complaint = any(
            re.search(pattern, feedback_lower)
            for pattern in self.MISSING_INDICATORS
        )

        if is_complaint:
            for element_type, patterns in self.ELEMENT_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, feedback_lower):
                        if element_type not in result["missing_elements"]:
                            result["missing_elements"].append(element_type)

        # Détecter les problèmes de qualité
        for indicator in self.QUALITY_INDICATORS:
            if re.search(indicator, feedback_lower):
                # Identifier quel élément pose problème
                for element_type, patterns in self.ELEMENT_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, feedback_lower):
                            result["quality_issues"].append({
                                "element": element_type,
                                "issue": "unclear"
                            })
                            break

        # Enregistrer dans l'historique
        self.feedback_history.append(result)

        # Mettre à jour la mémoire de savoir si disponible
        if self.knowledge_memory and result["missing_elements"]:
            self._update_knowledge_memory(result)

        return result

    def identify_missing_elements(self, feedback_text: str) -> List[str]:
        """
        Version simplifiée pour identifier uniquement les éléments manquants

        Args:
            feedback_text: Texte de feedback

        Returns:
            Liste des types d'éléments manquants
        """
        result = self.parse_feedback_text(feedback_text)
        return result["missing_elements"]

    def _detect_sentiment(self, text: str) -> str:
        """Détecte le sentiment général du feedback"""
        positive_words = ["bien", "super", "parfait", "merci", "top", "génial", "utile"]
        negative_words = ["nul", "mauvais", "inutile", "horrible", "décevant", "frustrant"]

        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def _update_knowledge_memory(self, parsed_feedback: Dict):
        """Met à jour la mémoire de savoir avec le feedback"""
        if not self.knowledge_memory:
            return

        subject = parsed_feedback.get("subject")
        topic = parsed_feedback.get("topic", "general")

        for element in parsed_feedback["missing_elements"]:
            self.knowledge_memory.record_missing_element(
                subject=subject,
                topic=topic,
                element_type=element
            )

    def get_enrichment_suggestions(self, subject: str, topic: str = None) -> List[Dict]:
        """
        Génère des suggestions d'enrichissement basées sur le feedback historique

        Args:
            subject: Matière
            topic: Thème spécifique (optionnel)

        Returns:
            Liste de suggestions avec priorité
        """
        # Filtrer le feedback pertinent
        relevant_feedback = [
            f for f in self.feedback_history
            if f.get("subject") == subject and (topic is None or f.get("topic") == topic)
        ]

        if not relevant_feedback:
            return []

        # Compter les éléments manquants
        missing_counts = {}
        for feedback in relevant_feedback:
            for element in feedback.get("missing_elements", []):
                missing_counts[element] = missing_counts.get(element, 0) + 1

        # Générer les suggestions triées par fréquence
        suggestions = []
        for element, count in sorted(missing_counts.items(), key=lambda x: x[1], reverse=True):
            priority = "high" if count >= 3 else "medium" if count >= 2 else "low"
            suggestions.append({
                "element_type": element,
                "times_requested": count,
                "priority": priority,
                "action": self._get_enrichment_action(element)
            })

        return suggestions

    def _get_enrichment_action(self, element_type: str) -> str:
        """Retourne l'action recommandée pour enrichir un type d'élément"""
        actions = {
            "dates": "Ajouter une frise chronologique avec les dates clés",
            "figures": "Inclure les personnages/auteurs importants avec leur rôle",
            "definitions": "Ajouter un glossaire avec définitions claires",
            "formulas": "Inclure les formules avec exemples d'application",
            "examples": "Ajouter des exemples concrets et résolus",
            "methodology": "Détailler les étapes méthodologiques",
            "context": "Expliquer le contexte et les causes/conséquences",
            "summary": "Ajouter un résumé des points essentiels"
        }
        return actions.get(element_type, f"Enrichir avec plus de {element_type}")

    def analyze_feedback_trends(self, last_n: int = 20) -> Dict:
        """
        Analyse les tendances globales du feedback pédagogique

        Returns:
            Dict avec statistiques et recommandations
        """
        recent = self.feedback_history[-last_n:] if self.feedback_history else []

        if not recent:
            return {"total_feedback": 0, "trends": []}

        # Compter les éléments manquants globalement
        all_missing = {}
        subjects_affected = {}

        for feedback in recent:
            for element in feedback.get("missing_elements", []):
                all_missing[element] = all_missing.get(element, 0) + 1

            subject = feedback.get("subject")
            if subject:
                subjects_affected[subject] = subjects_affected.get(subject, 0) + 1

        # Analyser le sentiment
        sentiments = [f.get("sentiment", "neutral") for f in recent]
        sentiment_distribution = {
            "positive": sentiments.count("positive"),
            "neutral": sentiments.count("neutral"),
            "negative": sentiments.count("negative")
        }

        return {
            "total_feedback": len(recent),
            "most_missing_elements": sorted(all_missing.items(), key=lambda x: x[1], reverse=True)[:5],
            "subjects_needing_attention": sorted(subjects_affected.items(), key=lambda x: x[1], reverse=True)[:3],
            "sentiment_distribution": sentiment_distribution,
            "overall_satisfaction": "good" if sentiment_distribution["positive"] > sentiment_distribution["negative"] else "needs_improvement"
        }

    def get_quick_fixes(self, subject: str) -> List[str]:
        """
        Retourne des corrections rapides basées sur le feedback fréquent

        Args:
            subject: Matière concernée

        Returns:
            Liste de corrections à appliquer
        """
        suggestions = self.get_enrichment_suggestions(subject)

        quick_fixes = []
        for suggestion in suggestions[:3]:  # Top 3
            if suggestion["priority"] == "high":
                quick_fixes.append(suggestion["action"])

        return quick_fixes
