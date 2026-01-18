"""
Planificateur de tâches - Décomposition intelligente avec système Goblin-style
"""
import re
import time
from typing import Dict, List, Optional

from config.settings import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, ANTHROPIC_API_URL, API_TIMEOUT
from config.tdah_rules import TDAH_RULES, SPICINESS_LEVELS, CATEGORY_CONFIG


class GoblinStyleDecomposer:
    """Décomposeur inspiré de Goblin Tools avec recherche web enrichie"""

    @staticmethod
    def decompose_with_spiciness(
        task_description: str,
        spiciness: int = 3,
        context: Dict = None,
        web_context: Dict = None,
        use_api: bool = True
    ) -> List[Dict]:
        """
        Décompose une tâche avec niveau spiciness + enrichissement web

        Args:
            task_description: Description de la tâche
            spiciness: Niveau de détail (1-5)
            context: Contexte analysé (optionnel)
            web_context: Contexte web enrichi (optionnel)
            use_api: Utiliser l'API si disponible
        """
        if context is None:
            from core.task_analyzer import TaskAnalyzer
            context = TaskAnalyzer.analyze_context(task_description)

        spicy_config = SPICINESS_LEVELS.get(spiciness, SPICINESS_LEVELS[3])
        max_tasks = spicy_config["max_subtasks"]
        detail_mult = spicy_config["detail_multiplier"]

        # Essayer l'API si disponible
        if use_api and ANTHROPIC_API_KEY:
            try:
                import requests
                prompt = GoblinStyleDecomposer.build_spicy_prompt(
                    task_description, context, spiciness, max_tasks, detail_mult, web_context
                )

                response = requests.post(
                    ANTHROPIC_API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": ANTHROPIC_MODEL,
                        "max_tokens": 3000,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=API_TIMEOUT
                )

                if response.status_code == 200:
                    data = response.json()
                    text = next((c["text"] for c in data.get("content", []) if c.get("type") == "text"), "")
                    return GoblinStyleDecomposer.parse_response(text, task_description, context, max_tasks)

            except Exception as e:
                print(f"⚠️ Erreur API: {e}")

        # Fallback offline
        print(f"⚠️ Mode hors ligne - Décomposition {spicy_config['label']}")
        return GoblinStyleDecomposer.get_fallback_with_spiciness(task_description, context, spiciness)

    @staticmethod
    def build_spicy_prompt(
        task: str,
        context: Dict,
        spiciness: int,
        max_tasks: int,
        detail_mult: float,
        web_context: Dict = None
    ) -> str:
        """Construit un prompt enrichi par la recherche web"""
        spicy_config = SPICINESS_LEVELS[spiciness]
        level = context.get("level", "premiere")
        web_context = web_context or {}

        # Déterminer le tier éducatif
        from core.task_analyzer import TaskAnalyzer
        tier = TaskAnalyzer.get_level_tier(level)
        tier_labels = {"college": "COLLÈGE", "lycee": "LYCÉE", "universite": "UNIVERSITÉ"}
        tier_label = tier_labels.get(tier, "LYCÉE")

        base_instructions = f"""Tu es un EXPERT en décomposition de tâches pour personnes TDAH.

🌶️ NIVEAU DE DÉTAIL : {spicy_config['label']} ({spicy_config['emoji']})
{spicy_config['description']}

🎓 NIVEAU SCOLAIRE : {tier_label} ({level.upper()})

📚 ADAPTATION OBLIGATOIRE AU NIVEAU SCOLAIRE :"""

        # Instructions spécifiques au niveau scolaire
        school_instructions = GoblinStyleDecomposer._get_school_instructions(tier)
        base_instructions += school_instructions

        # Ajout des informations web si disponibles
        if web_context.get("found_resources"):
            web_info = "\n\n🔍 MÉTHODOLOGIE SPÉCIFIQUE (basée sur recherches) :\n"

            key_concepts = web_context.get("key_concepts", [])
            if key_concepts:
                web_info += f"Concepts clés : {', '.join(key_concepts[:3])}\n"

            methodology = web_context.get("methodology_hints", [])
            if methodology:
                web_info += "\nCONSEILS MÉTHODOLOGIQUES À INTÉGRER :\n"
                for hint in methodology[:5]:
                    web_info += f"- {hint}\n"

            mistakes = web_context.get("common_mistakes", [])
            if mistakes:
                web_info += "\nERREURS FRÉQUENTES À ÉVITER :\n"
                for mistake in mistakes[:3]:
                    web_info += f"⚠️ {mistake}\n"

            base_instructions += web_info

        # Instructions de détail
        detail_instruction = GoblinStyleDecomposer._get_detail_instructions(spiciness, max_tasks)

        subject_instr = ""
        if context.get("subject") == "maths":
            subject_instr = "\n📐 MATHS : Séparer calculs / vérification / correction"
        elif context.get("subject") in ["français", "anglais", "espagnol"]:
            subject_instr = "\n📚 LANGUE : Séparer vocabulaire / grammaire / rédaction"

        urgency = ""
        if context.get("time_constraint") == "urgent":
            urgency = "\n⚠️ URGENT : Prioriser l'essentiel, pas de détails superflus"

        prompt = f"""{base_instructions}

{detail_instruction}
{subject_instr}
{urgency}

📚 MATIÈRE : {context.get('subject', 'autre').upper()}
🎯 TYPE : {context.get('type', 'autre').upper()}
🎓 NIVEAU : {context.get('level', 'autre').upper()}

📋 TÂCHE À DÉCOMPOSER :
"{task}"

🎯 RÈGLES ABSOLUES :
1. EXACTEMENT {max_tasks} étapes maximum (pas plus !)
2. UN verbe d'action au début
3. Quantités précises (pages, exercices, minutes)
4. Phrases courtes (10 mots max)
5. Ordre logique progressif

RÉPONDS UNIQUEMENT avec la liste numérotée :
"1. [ACTION]"

NE METS RIEN D'AUTRE."""

        return prompt

    @staticmethod
    def _get_school_instructions(tier: str) -> str:
        """Retourne les instructions spécifiques au niveau scolaire"""
        if tier == "college":
            return """
**COLLÈGE (11-15 ans) - SIMPLIFICATION MAXIMALE :**
- Vocabulaire SIMPLE comme pour un enfant
- Phrases ULTRA-COURTES (5-8 mots MAX)
- Verbes d'action basiques : lire, écrire, faire, noter, chercher
- Consignes CONCRÈTES (jamais abstrait)
- Temps COURTS (5-15 min max par étape)
- Ton ENCOURAGEANT et positif
"""
        elif tier == "lycee":
            return """
**LYCÉE (15-18 ans) - ÉQUILIBRE :**
- Vocabulaire standard mais clair
- Phrases moyennes (8-12 mots)
- Méthode explicite
- Consignes précises avec contexte
- Temps moyens (10-25 min par étape)
"""
        else:  # université
            return """
**UNIVERSITÉ (18+ ans) - AUTONOMIE GUIDÉE :**
- Vocabulaire académique autorisé
- Phrases complètes et précises
- Méthodologie rigoureuse
- Approche analytique
- Temps flexibles (15-30 min par étape)
"""

    @staticmethod
    def _get_detail_instructions(spiciness: int, max_tasks: int) -> str:
        """Retourne les instructions de niveau de détail"""
        instructions = {
            1: f"- MAX {max_tasks} étapes ESSENTIELLES\n- Regrouper au maximum\n- Chaque étape = 20-30 min",
            2: f"- MAX {max_tasks} étapes PRINCIPALES\n- Garder les étapes importantes\n- Chaque étape = 15-25 min",
            3: f"- MAX {max_tasks} étapes ÉQUILIBRÉES\n- Ni trop vague, ni trop détaillé\n- Chaque étape = 10-20 min",
            4: f"- MAX {max_tasks} étapes DÉTAILLÉES\n- Précision accrue\n- Chaque étape = 8-15 min",
            5: f"- MAX {max_tasks} MICRO-ÉTAPES\n- Décomposition maximale\n- Chaque étape = 5-10 min"
        }
        return instructions.get(spiciness, instructions[3])

    @staticmethod
    def get_fallback_with_spiciness(task: str, context: Dict, spiciness: int) -> List[Dict]:
        """Fallback intelligent adapté au spiciness ET au niveau scolaire"""
        spicy_config = SPICINESS_LEVELS[spiciness]
        max_tasks = spicy_config["max_subtasks"]
        level = context.get("level", "premiere")

        from core.task_analyzer import TaskAnalyzer
        tier = TaskAnalyzer.get_level_tier(level)

        # Générer les tâches selon tier et spiciness
        tasks = GoblinStyleDecomposer._generate_fallback_tasks(tier, spiciness)[:max_tasks]

        return [
            {
                "id": f"task-{int(time.time() * 1000)}-{idx}",
                "title": t["title"],
                "category": t["category"],
                "difficulty": t["difficulty"],
                "estimatedTime": 0,
                "completed": False
            }
            for idx, t in enumerate(tasks)
        ]

    @staticmethod
    def _generate_fallback_tasks(tier: str, spiciness: int) -> List[Dict]:
        """Génère des tâches de fallback selon le tier et le spiciness"""
        if spiciness <= 2:
            if tier == "college":
                return [
                    {"title": "Lire 2 fois ce qu'il faut faire", "category": "lecture", "difficulty": "easy"},
                    {"title": "Préparer ton matériel (5 min)", "category": "organisation", "difficulty": "easy"},
                    {"title": "Faire l'exercice", "category": "exercices", "difficulty": "medium"},
                    {"title": "Vérifier ton travail", "category": "revision", "difficulty": "easy"}
                ]
            elif tier == "lycee":
                return [
                    {"title": "Comprendre l'énoncé global (lire 2x)", "category": "lecture", "difficulty": "easy"},
                    {"title": "Rassembler matériel nécessaire (5 min)", "category": "organisation", "difficulty": "easy"},
                    {"title": "Faire partie principale", "category": "exercices", "difficulty": "medium"},
                    {"title": "Vérifier et finaliser", "category": "revision", "difficulty": "easy"}
                ]
            else:
                return [
                    {"title": "Analyser problématique et contraintes", "category": "lecture", "difficulty": "easy"},
                    {"title": "Rassembler sources et références", "category": "recherche", "difficulty": "easy"},
                    {"title": "Développer argumentation principale", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Réviser et affiner contenu", "category": "revision", "difficulty": "easy"}
                ]
        elif spiciness == 3:
            if tier == "college":
                return [
                    {"title": "Lire ce qu'il faut faire", "category": "lecture", "difficulty": "easy"},
                    {"title": "Préparer ton matériel (5 min)", "category": "organisation", "difficulty": "easy"},
                    {"title": "Faire la première partie", "category": "exercices", "difficulty": "medium"},
                    {"title": "Vérifier ce que tu as fait", "category": "revision", "difficulty": "easy"},
                    {"title": "Faire la deuxième partie", "category": "exercices", "difficulty": "medium"},
                    {"title": "Tout relire et corriger", "category": "revision", "difficulty": "easy"}
                ]
            elif tier == "lycee":
                return [
                    {"title": "Lire énoncé et noter 3 points clés", "category": "lecture", "difficulty": "easy"},
                    {"title": "Rassembler matériel (timer 5 min)", "category": "organisation", "difficulty": "easy"},
                    {"title": "Faire première partie", "category": "exercices", "difficulty": "medium"},
                    {"title": "Vérifier première partie", "category": "revision", "difficulty": "easy"},
                    {"title": "Faire deuxième partie", "category": "exercices", "difficulty": "medium"},
                    {"title": "Relire et corriger", "category": "revision", "difficulty": "easy"}
                ]
            else:
                return [
                    {"title": "Analyser consigne et identifier enjeux", "category": "lecture", "difficulty": "easy"},
                    {"title": "Rassembler corpus documentaire", "category": "recherche", "difficulty": "easy"},
                    {"title": "Élaborer plan structuré", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Rédiger développement argumenté", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Intégrer références bibliographiques", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Réviser cohérence et rigueur", "category": "revision", "difficulty": "easy"}
                ]
        else:  # spiciness 4-5
            if tier == "college":
                return [
                    {"title": "Lire une première fois", "category": "lecture", "difficulty": "easy"},
                    {"title": "Surligner les mots importants", "category": "lecture", "difficulty": "easy"},
                    {"title": "Noter 3 choses à faire", "category": "ecriture", "difficulty": "easy"},
                    {"title": "Chercher ton cahier", "category": "organisation", "difficulty": "easy"},
                    {"title": "Installer ton bureau", "category": "organisation", "difficulty": "easy"},
                    {"title": "Commencer partie 1 (10 min)", "category": "exercices", "difficulty": "medium"},
                    {"title": "Pause 2 min + vérifier", "category": "pause", "difficulty": "easy"},
                    {"title": "Faire partie 2 (10 min)", "category": "exercices", "difficulty": "medium"},
                    {"title": "Tout relire (5 min)", "category": "revision", "difficulty": "easy"}
                ]
            elif tier == "lycee":
                return [
                    {"title": "Lire énoncé une première fois", "category": "lecture", "difficulty": "easy"},
                    {"title": "Surligner mots-clés de l'énoncé", "category": "lecture", "difficulty": "easy"},
                    {"title": "Noter 3-5 points principaux", "category": "ecriture", "difficulty": "easy"},
                    {"title": "Chercher matériel (livres, cahiers)", "category": "organisation", "difficulty": "easy"},
                    {"title": "Installer espace de travail", "category": "organisation", "difficulty": "easy"},
                    {"title": "Commencer partie 1 (timer 15 min)", "category": "exercices", "difficulty": "medium"},
                    {"title": "Pause 2 min + vérif partie 1", "category": "pause", "difficulty": "easy"},
                    {"title": "Faire partie 2 (timer 15 min)", "category": "exercices", "difficulty": "medium"},
                    {"title": "Relire ensemble (timer 5 min)", "category": "revision", "difficulty": "easy"}
                ]
            else:
                return [
                    {"title": "Lecture analytique consigne complète", "category": "lecture", "difficulty": "easy"},
                    {"title": "Identification problématique centrale", "category": "lecture", "difficulty": "easy"},
                    {"title": "Recherche sources primaires pertinentes", "category": "recherche", "difficulty": "easy"},
                    {"title": "Cartographie concepts-clés", "category": "ecriture", "difficulty": "easy"},
                    {"title": "Élaboration architecture argumentative", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Rédaction introduction problématisée", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Développement partie 1 avec références", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Pause réflexive + vérification cohérence", "category": "pause", "difficulty": "easy"},
                    {"title": "Développement parties 2-3", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Synthèse critique et ouverture", "category": "ecriture", "difficulty": "medium"},
                    {"title": "Révision rigueur académique", "category": "revision", "difficulty": "easy"}
                ]

    @staticmethod
    def parse_response(text: str, original_task: str, context: Dict, max_tasks: int) -> List[Dict]:
        """Parse la réponse de l'IA"""
        lines = [
            re.sub(r'^\d+\.\s*', '', line.strip())
            for line in text.split('\n')
            if re.match(r'^\d+\.', line.strip())
        ]

        if not lines:
            return GoblinStyleDecomposer.get_fallback_with_spiciness(original_task, context, 3)

        lines = lines[:max_tasks]

        return [
            {
                "id": f"task-{int(time.time() * 1000)}-{idx}",
                "title": title,
                "category": SmartTaskDecomposer.detect_category(title),
                "difficulty": SmartTaskDecomposer.detect_difficulty(title),
                "estimatedTime": 0,
                "completed": False
            }
            for idx, title in enumerate(lines)
        ]


class SmartTaskDecomposer:
    """Décomposeur intelligent avec analyse contextuelle (maintenu pour compatibilité)"""

    @staticmethod
    def decompose(task_description: str, spiciness: int = 3) -> List[Dict]:
        """Décompose avec analyse contextuelle avancée"""
        from core.task_analyzer import TaskAnalyzer
        context = TaskAnalyzer.analyze_context(task_description)
        return GoblinStyleDecomposer.decompose_with_spiciness(task_description, spiciness, context)

    @staticmethod
    def detect_category(title: str) -> str:
        """Détecte la catégorie d'une tâche"""
        lower_title = title.lower()

        for category, config in CATEGORY_CONFIG.items():
            if any(keyword in lower_title for keyword in config["keywords"]):
                return category

        return "autre"

    @staticmethod
    def detect_difficulty(title: str) -> str:
        """Détecte la difficulté d'une tâche"""
        lower_title = title.lower()

        easy_keywords = ['lire', 'relire', 'noter', 'recopier', 'chercher', 'rassembler', 'surligner']
        hard_keywords = ['rédiger', 'créer', 'analyser', 'complexe', 'difficile', 'développer', 'argumenter']

        if any(word in lower_title for word in hard_keywords):
            return 'hard'
        if any(word in lower_title for word in easy_keywords):
            return 'easy'

        return 'medium'

    @staticmethod
    def auto_categorize_with_emoji(task_title: str) -> Dict:
        """Catégorisation automatique avancée avec emojis"""
        category = SmartTaskDecomposer.detect_category(task_title)
        config = CATEGORY_CONFIG.get(category, CATEGORY_CONFIG["autre"])

        return {
            "category": category,
            "emoji": config["emoji"],
            "color": config["color"]
        }
