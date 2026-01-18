"""
Mémoire de savoir - Stocke les lacunes et besoins par sujet/thème
Structure: {subject: {topic: {missing_often, priority, times_flagged}}}
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

from config.settings import KNOWLEDGE_MEMORY_FILE, DEFAULT_KNOWLEDGE_MEMORY, DATA_DIR


class KnowledgeMemory:
    """
    Mémoire intelligente des besoins pédagogiques par sujet/thème.

    Permet de :
    - Enregistrer les éléments souvent manquants
    - Prioriser les enrichissements
    - Injecter automatiquement les éléments nécessaires

    Structure des données :
    {
        "histoire": {
            "premiere_guerre_mondiale": {
                "missing_often": ["dates", "figures"],
                "priority": "high",
                "times_flagged": 4,
                "last_updated": "2024-01-15T10:30:00"
            }
        }
    }
    """

    PRIORITY_THRESHOLDS = {
        "high": 3,    # 3+ signalements
        "medium": 2,  # 2 signalements
        "low": 1      # 1 signalement
    }

    def __init__(self, memory_file: str = None):
        self.memory_file = memory_file or KNOWLEDGE_MEMORY_FILE
        self.memory = self.load_memory()

    def load_memory(self) -> Dict:
        """Charge la mémoire de savoir depuis le fichier"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)

            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Erreur chargement mémoire: {e}")

        return DEFAULT_KNOWLEDGE_MEMORY.copy()

    def save_memory(self):
        """Sauvegarde la mémoire de savoir"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde mémoire: {e}")

    # ========================================
    # ENREGISTREMENT DES LACUNES
    # ========================================

    def record_missing_element(
        self,
        subject: str,
        topic: str,
        element_type: str  # "dates", "figures", "definitions", "formulas", etc.
    ):
        """
        Enregistre un élément manquant pour un sujet/thème

        Args:
            subject: Matière (ex: "histoire")
            topic: Thème spécifique (ex: "premiere_guerre_mondiale")
            element_type: Type d'élément manquant
        """
        if not subject:
            return

        # Normaliser les clés
        subject = self._normalize_key(subject)
        topic = self._normalize_key(topic) if topic else "general"

        # Initialiser si nécessaire
        if subject not in self.memory:
            self.memory[subject] = {}

        if topic not in self.memory[subject]:
            self.memory[subject][topic] = {
                "missing_often": [],
                "priority": "low",
                "times_flagged": 0,
                "last_updated": None
            }

        topic_data = self.memory[subject][topic]

        # Ajouter l'élément s'il n'est pas déjà présent
        if element_type not in topic_data["missing_often"]:
            topic_data["missing_often"].append(element_type)

        # Incrémenter le compteur
        topic_data["times_flagged"] += 1

        # Mettre à jour la priorité
        topic_data["priority"] = self._calculate_priority(topic_data["times_flagged"])

        # Mettre à jour le timestamp
        topic_data["last_updated"] = datetime.now().isoformat()

        self.save_memory()

    def record_multiple_missing(
        self,
        subject: str,
        topic: str,
        elements: List[str]
    ):
        """Enregistre plusieurs éléments manquants en une fois"""
        for element in elements:
            self.record_missing_element(subject, topic, element)

    # ========================================
    # RÉCUPÉRATION DES DONNÉES
    # ========================================

    def get_topic_info(self, subject: str, topic: str) -> Optional[Dict]:
        """Retourne les infos d'un topic spécifique"""
        subject = self._normalize_key(subject)
        topic = self._normalize_key(topic) if topic else "general"

        if subject in self.memory and topic in self.memory[subject]:
            return self.memory[subject][topic]
        return None

    def get_missing_elements(self, subject: str, topic: str = None) -> List[str]:
        """
        Retourne les éléments souvent manquants pour un sujet

        Args:
            subject: Matière
            topic: Thème spécifique (optionnel)

        Returns:
            Liste des types d'éléments manquants
        """
        subject = self._normalize_key(subject)

        if subject not in self.memory:
            return []

        if topic:
            topic = self._normalize_key(topic)
            if topic in self.memory[subject]:
                return self.memory[subject][topic].get("missing_often", [])
            return []

        # Agréger tous les topics du sujet
        all_missing = set()
        for topic_data in self.memory[subject].values():
            all_missing.update(topic_data.get("missing_often", []))
        return list(all_missing)

    def get_priority_elements(self, subject: str, min_priority: str = "medium") -> List[Dict]:
        """
        Retourne les éléments prioritaires pour un sujet

        Args:
            subject: Matière
            min_priority: Priorité minimum ("low", "medium", "high")

        Returns:
            Liste des topics avec leurs éléments manquants, triés par priorité
        """
        subject = self._normalize_key(subject)

        if subject not in self.memory:
            return []

        priority_order = {"high": 0, "medium": 1, "low": 2}
        min_priority_value = priority_order.get(min_priority, 1)

        results = []
        for topic, data in self.memory[subject].items():
            topic_priority = data.get("priority", "low")
            if priority_order.get(topic_priority, 2) <= min_priority_value:
                results.append({
                    "topic": topic,
                    "missing_often": data.get("missing_often", []),
                    "priority": topic_priority,
                    "times_flagged": data.get("times_flagged", 0)
                })

        return sorted(results, key=lambda x: priority_order.get(x["priority"], 2))

    def should_inject_element(
        self,
        subject: str,
        topic: str,
        element_type: str
    ) -> bool:
        """
        Détermine si un élément doit être automatiquement injecté

        Args:
            subject: Matière
            topic: Thème
            element_type: Type d'élément

        Returns:
            True si l'élément doit être injecté
        """
        topic_info = self.get_topic_info(subject, topic)

        if not topic_info:
            return False

        # Injecter si l'élément est souvent manquant ET priorité >= medium
        is_often_missing = element_type in topic_info.get("missing_often", [])
        is_priority = topic_info.get("priority") in ["high", "medium"]

        return is_often_missing and is_priority

    def get_injection_list(self, subject: str, topic: str) -> List[str]:
        """
        Retourne la liste des éléments à injecter automatiquement

        Args:
            subject: Matière
            topic: Thème

        Returns:
            Liste des types d'éléments à injecter
        """
        topic_info = self.get_topic_info(subject, topic)

        if not topic_info:
            return []

        if topic_info.get("priority") in ["high", "medium"]:
            return topic_info.get("missing_often", [])

        return []

    # ========================================
    # GESTION DE LA MÉMOIRE
    # ========================================

    def clear_topic(self, subject: str, topic: str):
        """Efface les données d'un topic"""
        subject = self._normalize_key(subject)
        topic = self._normalize_key(topic)

        if subject in self.memory and topic in self.memory[subject]:
            del self.memory[subject][topic]
            self.save_memory()

    def clear_subject(self, subject: str):
        """Efface toutes les données d'un sujet"""
        subject = self._normalize_key(subject)

        if subject in self.memory:
            del self.memory[subject]
            self.save_memory()

    def reset_memory(self):
        """Réinitialise complètement la mémoire"""
        self.memory = DEFAULT_KNOWLEDGE_MEMORY.copy()
        self.save_memory()

    def decay_old_entries(self, days_threshold: int = 30):
        """
        Diminue la priorité des entrées anciennes

        Args:
            days_threshold: Nombre de jours avant décroissance
        """
        now = datetime.now()

        for subject in self.memory:
            for topic in self.memory[subject]:
                last_updated = self.memory[subject][topic].get("last_updated")
                if last_updated:
                    try:
                        last_date = datetime.fromisoformat(last_updated)
                        days_old = (now - last_date).days

                        if days_old > days_threshold:
                            # Réduire la priorité
                            current = self.memory[subject][topic].get("times_flagged", 0)
                            new_count = max(1, current - 1)
                            self.memory[subject][topic]["times_flagged"] = new_count
                            self.memory[subject][topic]["priority"] = self._calculate_priority(new_count)
                    except ValueError:
                        pass

        self.save_memory()

    # ========================================
    # STATISTIQUES
    # ========================================

    def get_statistics(self) -> Dict:
        """Retourne des statistiques sur la mémoire"""
        total_subjects = len(self.memory)
        total_topics = sum(len(topics) for topics in self.memory.values())

        all_missing = []
        for subject_data in self.memory.values():
            for topic_data in subject_data.values():
                all_missing.extend(topic_data.get("missing_often", []))

        # Compter les types d'éléments
        element_counts = {}
        for element in all_missing:
            element_counts[element] = element_counts.get(element, 0) + 1

        return {
            "total_subjects": total_subjects,
            "total_topics": total_topics,
            "most_common_missing": sorted(element_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "high_priority_topics": len([
                t for s in self.memory.values()
                for t in s.values()
                if t.get("priority") == "high"
            ])
        }

    # ========================================
    # HELPERS
    # ========================================

    def _normalize_key(self, key: str) -> str:
        """Normalise une clé (minuscules, underscores)"""
        if not key:
            return "general"
        return key.lower().replace(" ", "_").replace("-", "_")

    def _calculate_priority(self, times_flagged: int) -> str:
        """Calcule la priorité basée sur le nombre de signalements"""
        if times_flagged >= self.PRIORITY_THRESHOLDS["high"]:
            return "high"
        elif times_flagged >= self.PRIORITY_THRESHOLDS["medium"]:
            return "medium"
        return "low"
