"""
Règles TDAH, niveaux de spiciness et profils Pomodoro
"""

# ========================================
# RÈGLES TDAH
# ========================================
TDAH_RULES = {
    "MAX_TASK_DURATION": 30,  # minutes max par tâche
    "TIME_MARGIN": 1.25,  # marge de sécurité temps
    "MAX_SUBTASKS": 9,
    "MIN_SUBTASKS": 3,
    "DIFFICULTY_MULTIPLIER": {
        "easy": 1.0,
        "medium": 1.2,
        "hard": 1.5
    },
    "CATEGORY_BASE_TIME": {
        "lecture": 15,
        "ecriture": 25,
        "recherche": 20,
        "revision": 15,
        "exercices": 20,
        "organisation": 10,
        "pause": 5,
        "communication": 15,
        "apprentissage": 20,
        "creation": 25,
        "autre": 20
    }
}

# ========================================
# SYSTÈME DE SPICINESS (inspiré Goblin Tools)
# ========================================
SPICINESS_LEVELS = {
    1: {
        "emoji": "🌶️",
        "label": "Minimal",
        "max_subtasks": 3,
        "detail_multiplier": 0.5,
        "description": "Juste l'essentiel"
    },
    2: {
        "emoji": "🌶️🌶️",
        "label": "Léger",
        "max_subtasks": 5,
        "detail_multiplier": 0.75,
        "description": "Quelques étapes clés"
    },
    3: {
        "emoji": "🌶️🌶️🌶️",
        "label": "Moyen",
        "max_subtasks": 7,
        "detail_multiplier": 1.0,
        "description": "Décomposition équilibrée"
    },
    4: {
        "emoji": "🌶️🌶️🌶️🌶️",
        "label": "Détaillé",
        "max_subtasks": 9,
        "detail_multiplier": 1.3,
        "description": "Étapes bien détaillées"
    },
    5: {
        "emoji": "🌶️🌶️🌶️🌶️🌶️",
        "label": "Maximum",
        "max_subtasks": 12,
        "detail_multiplier": 1.6,
        "description": "Toutes les micro-étapes"
    }
}

# ========================================
# PROFILS POMODORO
# ========================================
POMODORO_PROFILES = {
    "classique": {
        "work": 25,
        "pause": 5,
        "label": "Classique (25/5)"
    },
    "tdah": {
        "work": 20,
        "pause": 5,
        "label": "TDAH doux (20/5)"
    },
    "fatigue": {
        "work": 15,
        "pause": 5,
        "label": "Fatigue (15/5)"
    },
    "intense": {
        "work": 45,
        "pause": 10,
        "label": "Intense (45/10)"
    },
    "micro": {
        "work": 10,
        "pause": 3,
        "label": "Micro (10/3)"
    }
}

# ========================================
# CATÉGORIES ET EMOJIS
# ========================================
CATEGORY_CONFIG = {
    "lecture": {
        "emoji": "📖",
        "keywords": ["lire", "relire", "parcourir", "consulter", "étudier texte"],
        "color": "blue"
    },
    "ecriture": {
        "emoji": "✏️",
        "keywords": ["écrire", "rédiger", "noter", "recopier", "créer", "composer", "plan"],
        "color": "purple"
    },
    "recherche": {
        "emoji": "🔍",
        "keywords": ["chercher", "recherche", "trouver", "google", "site", "documentation"],
        "color": "orange"
    },
    "revision": {
        "emoji": "📝",
        "keywords": ["réviser", "revoir", "vérifier", "corriger", "relecture", "réciter"],
        "color": "green"
    },
    "exercices": {
        "emoji": "🎯",
        "keywords": ["exercice", "faire", "résoudre", "calculer", "problème", "appliquer"],
        "color": "red"
    },
    "organisation": {
        "emoji": "📋",
        "keywords": ["rassembler", "organiser", "trier", "classer", "ranger", "préparer matériel"],
        "color": "gray"
    },
    "pause": {
        "emoji": "☕",
        "keywords": ["pause", "repos", "break", "boire", "étirer", "marcher"],
        "color": "brown"
    },
    "communication": {
        "emoji": "💬",
        "keywords": ["appeler", "contacter", "email", "message", "discussion", "réunion"],
        "color": "cyan"
    },
    "apprentissage": {
        "emoji": "🧠",
        "keywords": ["apprendre", "mémoriser", "comprendre", "assimiler", "retenir"],
        "color": "pink"
    },
    "creation": {
        "emoji": "🎨",
        "keywords": ["créer", "concevoir", "dessiner", "design", "inventer", "imaginer"],
        "color": "yellow"
    },
    "autre": {
        "emoji": "📌",
        "keywords": [],
        "color": "gray"
    }
}

# ========================================
# NIVEAUX SCOLAIRES
# ========================================
SCHOOL_LEVELS = {
    "college": ["6eme", "5eme", "4eme", "3eme"],
    "lycee": ["seconde", "premiere", "terminale"],
    "universite": ["L1", "L2", "L3"]
}

# ========================================
# MATIÈRES DÉTECTABLES
# ========================================
SUBJECTS = {
    "maths": ["math", "algèbre", "géométrie", "calcul", "équation", "dérivée", "fonction", "trigonométrie"],
    "physique": ["physique", "mécanique", "électricité", "optique", "force", "énergie", "circuit"],
    "chimie": ["chimie", "réaction", "molécule", "atome", "élément", "tableau périodique"],
    "svt": ["svt", "biologie", "cellule", "adn", "photosynthèse", "écosystème", "évolution"],
    "français": ["français", "littérature", "texte", "poème", "roman", "commentaire", "dissertation"],
    "histoire": ["histoire", "guerre", "révolution", "moyen âge", "antiquité", "empire", "roi"],
    "géographie": ["géographie", "géo", "continent", "pays", "climat", "population", "ville"],
    "anglais": ["anglais", "english"],
    "espagnol": ["espagnol", "español"],
    "allemand": ["allemand", "deutsch"],
    "philosophie": ["philo", "philosophie", "concept", "pensée", "conscience"],
    "economie": ["économie", "ses", "marché", "entreprise", "commerce"],
    "informatique": ["info", "informatique", "code", "python", "java", "algorithme", "programmation"]
}

# ========================================
# TYPES DE TÂCHES
# ========================================
TASK_TYPES = {
    "controle": ["contrôle", "ds", "test", "exam", "évaluation", "devoir surveillé"],
    "exposé": ["exposé", "présentation", "oral", "powerpoint", "diapo", "diaporama"],
    "dissertation": ["dissertation", "rédaction", "essai", "composition"],
    "exercices": ["exercice", "dm", "devoir maison", "td", "tp"],
    "lecture": ["lire", "lecture", "livre", "chapitre", "texte"],
    "révision": ["réviser", "révision", "apprendre", "revoir"],
    "recherche": ["recherche", "projet", "dossier", "enquête"],
    "commentaire": ["commentaire", "analyse", "étude de texte"],
    "fiche": ["fiche", "résumé", "synthèse"]
}
