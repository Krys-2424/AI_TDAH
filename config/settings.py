"""
Configuration globale de l'application Assistant TDAH
"""
import os

# ========================================
# CHEMINS DES FICHIERS
# ========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Fichiers de données
USER_PROFILE_FILE = os.path.join(DATA_DIR, "user_profile.json")
KNOWLEDGE_MEMORY_FILE = os.path.join(DATA_DIR, "knowledge_memory.json")
FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.json")
STATS_FILE = os.path.join(DATA_DIR, "stats.json")
USER_DATA_FILE = os.path.join(DATA_DIR, "user_data.json")

# ========================================
# CONFIGURATION API
# ========================================
# Anthropic API
ANTHROPIC_API_KEY = ""  # Mettre votre clé API Anthropic ici
ANTHROPIC_ADMIN_API_KEY = ""  # Clé API admin (optionnel)
ANTHROPIC_API_KEY_ID = ""  # ID de la clé API (optionnel)
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# Perplexity API
PERPLEXITY_API_KEY = ""  # Mettre votre clé API Perplexity ici
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_MODEL = "llama-3.1-sonar-small-128k-online"

# ========================================
# CONFIGURATION PAR DÉFAUT
# ========================================
DEFAULT_USER_PROFILE = {
    "preferred_spiciness": 3,
    "focus_duration": 20,
    "difficulty_bias": {
        "maths": 0,
        "histoire": 0,
        "physique": 0,
        "francais": 0,
        "anglais": 0
    },
    "fatigue_sensitivity": 0.5,
    "web_enabled": False,
    "preferred_hours": {},
    "subject_preferences": {},
    "total_tasks_completed": 0,
    "streak_days": 0,
    "last_session": None
}

DEFAULT_KNOWLEDGE_MEMORY = {}

DEFAULT_FEEDBACK = {
    "history": [],
    "form_feedback": [],
    "pedagogical_feedback": [],
    "last_session": None
}

DEFAULT_STATS = {
    "total_sessions": 0,
    "total_tasks_decomposed": 0,
    "total_tasks_completed": 0,
    "average_efficiency": 1.0,
    "subjects_worked": {},
    "best_hours": []
}

# ========================================
# TIMEOUTS ET LIMITES
# ========================================
API_TIMEOUT = 30  # secondes
MAX_RETRIES = 3
MAX_TASK_HISTORY = 100
MAX_FEEDBACK_HISTORY = 200
