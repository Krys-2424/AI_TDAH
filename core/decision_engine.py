"""
Moteur de décision - Chef d'orchestre qui décide quand utiliser web/local/mémoire
"""
from typing import Dict, List, Optional, Tuple
from enum import Enum


class DataSource(Enum):
    """Sources de données disponibles"""
    LOCAL_ENGINES = "local"      # Moteurs pédagogiques locaux
    KNOWLEDGE_MEMORY = "memory"  # Mémoire de savoir apprise
    WEB_PERPLEXITY = "web"       # Recherche web via Perplexity
    ANTHROPIC_API = "api"        # API Anthropic pour décomposition


class DecisionEngine:
    """
    Chef d'orchestre intelligent qui décide :
    - Quelle source utiliser pour répondre
    - Quand appeler le web
    - Comment combiner les sources

    Logique de décision :
    1. Si la question nécessite des données factuelles ET web autorisé -> web
    2. Si le sujet/thème est dans la mémoire -> mémoire + local
    3. Sinon -> moteurs locaux uniquement
    """

    # Mots-clés indiquant besoin de données factuelles
    FACTUAL_KEYWORDS = [
        "date", "année", "quand", "qui", "où",
        "combien", "chiffre", "statistique",
        "événement", "découverte", "invention"
    ]

    # Matières nécessitant souvent des données factuelles
    FACTUAL_SUBJECTS = ["histoire", "géographie", "svt", "physique", "chimie"]

    def __init__(
        self,
        user_personalization=None,
        knowledge_memory=None,
        web_guard=None
    ):
        """
        Args:
            user_personalization: Instance de UserPersonalization
            knowledge_memory: Instance de KnowledgeMemory
            web_guard: Instance de WebGuard
        """
        self.user_profile = user_personalization
        self.knowledge_memory = knowledge_memory
        self.web_guard = web_guard

    # ========================================
    # DÉCISION PRINCIPALE
    # ========================================

    def decide_source(
        self,
        task: str,
        subject: str,
        topic: str = None,
        force_web: bool = False,
        force_offline: bool = False
    ) -> Tuple[DataSource, Dict]:
        """
        Décide quelle source utiliser pour une tâche

        Args:
            task: Description de la tâche
            subject: Matière
            topic: Thème spécifique (optionnel)
            force_web: Forcer l'utilisation du web
            force_offline: Forcer le mode hors ligne

        Returns:
            Tuple (source recommandée, métadonnées de décision)
        """
        decision_metadata = {
            "task": task,
            "subject": subject,
            "topic": topic,
            "reasons": []
        }

        # Mode forcé hors ligne
        if force_offline:
            decision_metadata["reasons"].append("Mode hors ligne forcé")
            return DataSource.LOCAL_ENGINES, decision_metadata

        # Vérifier si web est autorisé
        web_allowed = self._can_use_web()

        # Mode forcé web (si autorisé)
        if force_web and web_allowed:
            decision_metadata["reasons"].append("Web forcé par l'utilisateur")
            return DataSource.WEB_PERPLEXITY, decision_metadata

        # Vérifier si la tâche nécessite des données factuelles
        needs_factual = self.requires_factual_data(task, subject)

        # Vérifier si on a des données en mémoire
        has_memory = self._check_memory_available(subject, topic)

        # Logique de décision
        if needs_factual and web_allowed:
            decision_metadata["reasons"].append("Données factuelles requises")
            decision_metadata["reasons"].append("Web autorisé")
            return DataSource.WEB_PERPLEXITY, decision_metadata

        if has_memory:
            decision_metadata["reasons"].append("Données disponibles en mémoire")
            return DataSource.KNOWLEDGE_MEMORY, decision_metadata

        # Défaut : moteurs locaux
        decision_metadata["reasons"].append("Utilisation des moteurs locaux")
        return DataSource.LOCAL_ENGINES, decision_metadata

    def orchestrate_response(
        self,
        task: str,
        subject: str,
        topic: str = None,
        context: Dict = None
    ) -> Dict:
        """
        Orchestre la génération d'une réponse complète

        Args:
            task: Description de la tâche
            subject: Matière
            topic: Thème
            context: Contexte analysé

        Returns:
            Dict avec les données de toutes les sources pertinentes
        """
        # Décider la source principale
        primary_source, metadata = self.decide_source(task, subject, topic)

        result = {
            "primary_source": primary_source.value,
            "decision_metadata": metadata,
            "local_data": {},
            "memory_data": {},
            "web_data": {},
            "combined_data": {}
        }

        # Toujours récupérer les données locales comme base
        result["local_data"] = self._get_local_data(subject, task)

        # Récupérer les données mémoire si disponibles
        if self.knowledge_memory:
            result["memory_data"] = self._get_memory_data(subject, topic)

        # Récupérer les données web si nécessaire et autorisé
        if primary_source == DataSource.WEB_PERPLEXITY:
            result["web_data"] = self._get_web_data(task, subject, topic)

        # Combiner les données
        result["combined_data"] = self._combine_data(
            result["local_data"],
            result["memory_data"],
            result["web_data"],
            primary_source
        )

        return result

    # ========================================
    # VÉRIFICATIONS
    # ========================================

    def requires_factual_data(self, task: str, subject: str) -> bool:
        """
        Détermine si la tâche nécessite des données factuelles

        Args:
            task: Description de la tâche
            subject: Matière

        Returns:
            True si des données factuelles sont requises
        """
        task_lower = task.lower()

        # Vérifier les mots-clés
        has_factual_keywords = any(kw in task_lower for kw in self.FACTUAL_KEYWORDS)

        # Vérifier la matière
        is_factual_subject = subject in self.FACTUAL_SUBJECTS

        # Vérifier des patterns spécifiques
        specific_patterns = [
            "quelle est la date",
            "qui a",
            "quand a eu lieu",
            "quel événement",
            "quelle formule",
            "quel théorème"
        ]
        has_specific_pattern = any(pattern in task_lower for pattern in specific_patterns)

        return has_factual_keywords or (is_factual_subject and has_specific_pattern)

    def _can_use_web(self) -> bool:
        """Vérifie si le web peut être utilisé"""
        # Vérifier le profil utilisateur
        if self.user_profile and not self.user_profile.web_enabled:
            return False

        # Vérifier le web guard
        if self.web_guard and not self.web_guard.can_use_web():
            return False

        return True

    def _check_memory_available(self, subject: str, topic: str = None) -> bool:
        """Vérifie si des données sont disponibles en mémoire"""
        if not self.knowledge_memory:
            return False

        # Vérifier si le sujet existe en mémoire
        missing = self.knowledge_memory.get_missing_elements(subject, topic)
        return len(missing) > 0

    # ========================================
    # RÉCUPÉRATION DES DONNÉES
    # ========================================

    def _get_local_data(self, subject: str, task: str) -> Dict:
        """Récupère les données des moteurs locaux"""
        from engines.base import SubjectEngineFactory

        engine = SubjectEngineFactory.get_engine(subject)

        # Obtenir les données statiques si disponibles
        data = {}
        if hasattr(engine, 'get_static_data'):
            data = engine.get_static_data(task, "premiere")  # Level par défaut

        return {
            "source": "local_engine",
            "engine": engine.__class__.__name__,
            "definitions": data.get("definitions", []),
            "formulas": data.get("formulas", []),
            "dates": data.get("dates", []),
            "figures": data.get("figures", []),
            "methodology": data.get("methodology", []),
            "common_mistakes": data.get("common_mistakes", [])
        }

    def _get_memory_data(self, subject: str, topic: str = None) -> Dict:
        """Récupère les données de la mémoire de savoir"""
        if not self.knowledge_memory:
            return {}

        missing_elements = self.knowledge_memory.get_missing_elements(subject, topic)
        injection_list = self.knowledge_memory.get_injection_list(subject, topic) if topic else []
        topic_info = self.knowledge_memory.get_topic_info(subject, topic) if topic else None

        return {
            "source": "knowledge_memory",
            "missing_often": missing_elements,
            "should_inject": injection_list,
            "priority": topic_info.get("priority") if topic_info else "low",
            "times_flagged": topic_info.get("times_flagged", 0) if topic_info else 0
        }

    def _get_web_data(self, task: str, subject: str, topic: str = None) -> Dict:
        """Récupère les données du web via Perplexity"""
        # Import tardif pour éviter les dépendances circulaires
        try:
            from external.perplexity_client import PerplexityClient

            client = PerplexityClient()
            result = client.enrich_topic(task, subject, topic)

            return {
                "source": "perplexity",
                "success": result.get("success", False),
                "definitions": result.get("definitions", []),
                "dates": result.get("dates", []),
                "formulas": result.get("formulas", []),
                "figures": result.get("figures", []),
                "facts": result.get("facts", [])
            }
        except Exception as e:
            print(f"⚠️ Erreur récupération web: {e}")
            return {"source": "perplexity", "success": False, "error": str(e)}

    def _combine_data(
        self,
        local_data: Dict,
        memory_data: Dict,
        web_data: Dict,
        primary_source: DataSource
    ) -> Dict:
        """
        Combine les données de toutes les sources

        Priorité :
        1. Web (si source principale)
        2. Local (données de base)
        3. Mémoire (enrichissement)
        """
        combined = {
            "definitions": [],
            "formulas": [],
            "dates": [],
            "figures": [],
            "methodology": [],
            "common_mistakes": [],
            "elements_to_inject": []
        }

        # Ajouter les données locales comme base
        if local_data:
            combined["definitions"].extend(local_data.get("definitions", []))
            combined["formulas"].extend(local_data.get("formulas", []))
            combined["dates"].extend(local_data.get("dates", []))
            combined["figures"].extend(local_data.get("figures", []))
            combined["methodology"].extend(local_data.get("methodology", []))
            combined["common_mistakes"].extend(local_data.get("common_mistakes", []))

        # Ajouter les données web (si disponibles et succès)
        if web_data and web_data.get("success"):
            # Fusionner sans dupliquer
            combined["definitions"] = self._merge_unique(
                combined["definitions"],
                web_data.get("definitions", []),
                key="term"
            )
            combined["dates"] = self._merge_unique(
                combined["dates"],
                web_data.get("dates", []),
                key="date"
            )
            combined["formulas"] = self._merge_unique(
                combined["formulas"],
                web_data.get("formulas", []),
                key="name"
            )
            combined["figures"] = self._merge_unique(
                combined["figures"],
                web_data.get("figures", []),
                key="name"
            )

        # Ajouter les éléments à injecter depuis la mémoire
        if memory_data:
            combined["elements_to_inject"] = memory_data.get("should_inject", [])

        return combined

    def _merge_unique(self, list1: List, list2: List, key: str = None) -> List:
        """Fusionne deux listes en évitant les doublons"""
        if not list2:
            return list1

        if key:
            # Fusion basée sur une clé
            existing_keys = {item.get(key) for item in list1 if isinstance(item, dict)}
            for item in list2:
                if isinstance(item, dict) and item.get(key) not in existing_keys:
                    list1.append(item)
                    existing_keys.add(item.get(key))
        else:
            # Fusion simple
            existing = set(str(item) for item in list1)
            for item in list2:
                if str(item) not in existing:
                    list1.append(item)

        return list1

    # ========================================
    # SUGGESTIONS
    # ========================================

    def suggest_web_usage(self, task: str, subject: str) -> Dict:
        """
        Suggère à l'utilisateur d'activer le web si pertinent

        Returns:
            Dict avec suggestion et raison
        """
        needs_factual = self.requires_factual_data(task, subject)
        web_enabled = self._can_use_web()

        if needs_factual and not web_enabled:
            return {
                "suggest_web": True,
                "reason": f"Cette tâche ({subject}) pourrait bénéficier de données actualisées du web.",
                "message": "Souhaites-tu activer la recherche web pour enrichir la réponse ?"
            }

        return {
            "suggest_web": False,
            "reason": "Les données locales sont suffisantes."
        }
