"""
Assistant TDAH Intelligent - Point d'entrée principal

Un système hybride adaptatif d'accompagnement scolaire pour élèves TDAH.
Fonctionne 100% hors ligne avec enrichissement web optionnel.
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.responsive_ui import ResponsiveUI, TDAHAssistant


def main():
    """Point d'entrée principal de l'application"""
    print("=" * 50)
    print("🧠 Assistant TDAH Intelligent")
    print("=" * 50)
    print()
    print("Initialisation des modules...")

    # Créer l'interface (qui crée l'assistant internalement)
    ui = ResponsiveUI()

    # Afficher le statut via l'assistant de l'UI
    print(f"✓ Profil utilisateur chargé")
    print(f"  - Spiciness préféré: {ui.assistant.personalization.preferred_spiciness}")
    print(f"  - Durée focus: {ui.assistant.personalization.focus_duration} min")
    print(f"  - Web activé: {'Oui' if ui.assistant.personalization.web_enabled else 'Non'}")
    print()

    print(f"✓ Mémoire pédagogique chargée")
    memory_subjects = len(ui.assistant.knowledge_memory.memory)
    print(f"  - {memory_subjects} matière(s) en mémoire")
    print()

    from external.perplexity_client import PerplexityClient
    perplexity = PerplexityClient()
    if perplexity.is_available():
        print("✓ API Perplexity configurée")
    else:
        print("○ API Perplexity non configurée (mode offline)")
    print()

    print("Démarrage de l'interface graphique...")
    print("-" * 50)

    # Lancer l'interface
    ui.run()

    print()
    print("-" * 50)
    print("Session terminée. À bientôt ! 👋")


def run_cli_mode():
    """Mode ligne de commande pour tests rapides"""
    print("🧠 Assistant TDAH - Mode CLI")
    print("-" * 30)

    assistant = TDAHAssistant()

    while True:
        print()
        task = input("📝 Décris ta tâche (ou 'quit' pour quitter): ").strip()

        if task.lower() in ['quit', 'exit', 'q']:
            break

        if not task:
            continue

        print()
        print("Analyse en cours...")

        # Analyser et décomposer
        result = assistant.process_task(task)

        if result.get("success"):
            print()
            print("=" * 40)
            print("📋 Plan de travail:")
            print("=" * 40)

            for i, subtask in enumerate(result.get("subtasks", []), 1):
                title = subtask.get("title", subtask.get("task", "Tâche"))
                duration = subtask.get("duration", "?")
                difficulty = subtask.get("difficulty", "medium")

                emoji = "🟢" if difficulty == "easy" else "🟡" if difficulty == "medium" else "🔴"
                print(f"{i}. {emoji} {title} ({duration} min)")

            print()
            total_time = sum(s.get("duration", 0) for s in result.get("subtasks", []))
            print(f"⏱️ Durée totale estimée: {total_time} minutes")

            if result.get("enriched_with_web"):
                print("🌐 Enrichi avec données web")

            if result.get("memory_injections"):
                print(f"💡 Éléments rappelés: {', '.join(result['memory_injections'])}")
        else:
            print("❌ Erreur lors de l'analyse")
            print(result.get("error", "Erreur inconnue"))


if __name__ == "__main__":
    # Vérifier les arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli_mode()
    else:
        main()
