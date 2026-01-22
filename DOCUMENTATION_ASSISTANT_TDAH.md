# Documentation Complete - Assistant TDAH Intelligent

## Table des matieres

1. [Presentation du projet](#1-presentation-du-projet)
2. [Technologies utilisees](#2-technologies-utilisees)
3. [Structure du fichier](#3-structure-du-fichier)
4. [Guide de reproduction pas a pas](#4-guide-de-reproduction-pas-a-pas)
5. [Fonctionnalites detaillees](#5-fonctionnalites-detaillees)
6. [Code CSS complet](#6-code-css-complet)
7. [Code JavaScript complet](#7-code-javascript-complet)
8. [Personnalisation](#8-personnalisation)

---

## 1. Presentation du projet

### Objectif
L'Assistant TDAH Intelligent est une application web concu pour aider les personnes atteintes de TDAH (Trouble du Deficit de l'Attention avec ou sans Hyperactivite) a :
- Decomposer leurs taches complexes en etapes simples
- Gerer leur temps avec un minuteur Pomodoro
- Obtenir des conseils adaptes
- Generer des fiches de revision personnalisees

### Fonctionnalites principales
1. **Decomposition de taches** : L'IA decompose une tache complexe en sous-etapes
2. **Systeme de felicitations** : Animation avec confettis quand toutes les taches sont completees
3. **Minuteur Pomodoro** : Timer configurable avec pauses courtes/longues
4. **Conseils TDAH** : Conseils pre-enregistres + generation IA
5. **Fiches de revision** : Generation dynamique adaptee au sujet et au niveau scolaire
6. **Systeme de feedback** : Notation et retours pour ameliorer les fiches futures
7. **Theme clair/sombre** : Basculement automatique ou manuel
8. **Traduction FR/EN** : Interface bilingue francais/anglais avec sauvegarde de preference

---

## 2. Technologies utilisees

### Frontend
- **HTML5** : Structure de la page
- **CSS3** : Styles, animations, variables CSS pour les themes
- **JavaScript (ES6+)** : Logique applicative, async/await

### API externe
- **Puter.js** : API d'intelligence artificielle gratuite
  - URL : `https://js.puter.com/v2/`
  - Fonction utilisee : `puter.ai.chat(prompt)`
  - Pas besoin de cle API (authentification via popup)

### Stockage
- **localStorage** : Sauvegarde des preferences (theme, langue, niveau scolaire, historique des fiches, feedbacks)

---

## 3. Structure du fichier

```
assistant_tdah.html
|
|-- <head>
|   |-- Meta tags
|   |-- Script Puter.js
|   |-- Styles CSS (inline)
|
|-- <body>
    |-- Bouton langue FR/EN (position fixe)
    |-- Bouton theme clair/sombre (position fixe)
    |-- Container principal
        |-- Header (titre + description)
        |-- Navigation par onglets
        |-- Onglet 1 : Taches
        |-- Onglet 2 : Pomodoro
        |-- Onglet 3 : Conseils
        |-- Onglet 4 : A connaitre
    |-- Scripts JavaScript (inline)
```

---

## 4. Guide de reproduction pas a pas

### Etape 1 : Creer le fichier HTML de base

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assistant TDAH Intelligent</title>
    <script src="https://js.puter.com/v2/"></script>
    <style>
        /* Les styles viendront ici */
    </style>
</head>
<body>
    <!-- Le contenu viendra ici -->
    <script>
        // Le JavaScript viendra ici
    </script>
</body>
</html>
```

### Etape 2 : Ajouter les variables CSS pour les themes

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    /* Mode sombre (par defaut) */
    --bg-primary: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    --bg-secondary: rgba(255, 255, 255, 0.1);
    --bg-tertiary: rgba(255, 255, 255, 0.05);
    --text-primary: #fff;
    --text-secondary: #a0a0a0;
    --text-muted: #888;
    --text-conseil: #ccc;
    --accent-primary: #667eea;
    --accent-secondary: #764ba2;
    --border-color: rgba(255, 255, 255, 0.1);
    --input-bg: rgba(255, 255, 255, 0.1);
    --shadow-color: rgba(0, 0, 0, 0.3);
}

[data-theme="light"] {
    /* Mode clair */
    --bg-primary: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    --bg-secondary: rgba(0, 0, 0, 0.05);
    --bg-tertiary: rgba(0, 0, 0, 0.03);
    --text-primary: #1a1a2e;
    --text-secondary: #555;
    --text-muted: #777;
    --text-conseil: #444;
    --accent-primary: #667eea;
    --accent-secondary: #764ba2;
    --border-color: rgba(0, 0, 0, 0.1);
    --input-bg: rgba(0, 0, 0, 0.05);
    --shadow-color: rgba(0, 0, 0, 0.15);
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: var(--bg-primary);
    min-height: 100vh;
    color: var(--text-primary);
    padding: 20px;
    transition: all 0.3s ease;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}
```

### Etape 3 : Creer la structure HTML principale

```html
<body>
    <!-- Bouton de basculement langue -->
    <button class="lang-toggle" id="lang-toggle" title="Switch to English">
        <span id="lang-icon">EN</span>
    </button>

    <!-- Bouton de basculement theme -->
    <button class="theme-toggle" id="theme-toggle" title="Changer de theme">
        <span id="theme-icon">&#9790;</span>
    </button>

    <div class="container">
        <header>
            <h1>Assistant TDAH Intelligent</h1>
            <p>Decompose tes taches, gere ton temps et decouvre des conseils adaptes</p>
        </header>

        <!-- Navigation par onglets -->
        <div class="nav-tabs">
            <button class="nav-tab active" data-tab="taches">Taches</button>
            <button class="nav-tab" data-tab="pomodoro">Pomodoro</button>
            <button class="nav-tab" data-tab="conseils">Conseils</button>
            <button class="nav-tab" data-tab="connaitre">A connaitre</button>
        </div>

        <!-- Contenu des onglets -->
        <div class="tab-content active" id="tab-taches">
            <!-- Contenu onglet Taches -->
        </div>

        <div class="tab-content" id="tab-pomodoro">
            <!-- Contenu onglet Pomodoro -->
        </div>

        <div class="tab-content" id="tab-conseils">
            <!-- Contenu onglet Conseils -->
        </div>

        <div class="tab-content" id="tab-connaitre">
            <!-- Contenu onglet A connaitre -->
        </div>
    </div>
</body>
```

### Etape 4 : Creer l'onglet "Taches"

```html
<div class="tab-content active" id="tab-taches">
    <div class="input-section">
        <label for="task-input">Decris ta tache :</label>
        <textarea id="task-input" placeholder="Ex: Faire ma dissertation de francais sur le romantisme pour lundi..."></textarea>

        <!-- Slider niveau de detail -->
        <div class="spiciness-section">
            <div class="spiciness-label">
                <span>Niveau de detail</span>
                <span id="spiciness-value">3</span>
            </div>
            <input type="range" min="1" max="5" value="3" class="spiciness-slider" id="spiciness-slider">
            <div class="spiciness-display" id="spiciness-display">Equilibre</div>
        </div>

        <button class="btn btn-primary" id="decompose-btn">Decomposer ma tache</button>
    </div>

    <!-- Section resultats -->
    <div class="results-section" id="results-section">
        <div class="loading" id="loading" style="display: none;">
            <div class="loading-spinner"></div>
            <p>Analyse en cours avec l'IA...</p>
        </div>

        <div id="results-content">
            <div class="results-header">
                <h2>Ton plan de travail</h2>
                <span id="task-count"></span>
            </div>
            <ul class="task-list" id="task-list"></ul>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" id="total-tasks">0</div>
                    <div class="stat-label">Etapes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="completed-tasks">0</div>
                    <div class="stat-label">Terminees</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="progress">0%</div>
                    <div class="stat-label">Progression</div>
                </div>
            </div>
        </div>

        <div class="error" id="error-message" style="display: none;"></div>
    </div>
</div>
```

### Etape 5 : Creer l'onglet "Pomodoro"

```html
<div class="tab-content" id="tab-pomodoro">
    <div class="pomodoro-section">
        <h2>Minuteur Pomodoro</h2>
        <div class="timer-status" id="timer-status">Pret a travailler</div>
        <div class="timer-display" id="timer-display">25:00</div>

        <div class="timer-buttons">
            <button class="btn-timer btn-start" id="btn-start">Demarrer</button>
            <button class="btn-timer btn-pause" id="btn-pause" style="display: none;">Pause</button>
            <button class="btn-timer btn-reset" id="btn-reset">Reinitialiser</button>
        </div>

        <div class="pomodoro-settings">
            <div class="setting-item">
                <label>Travail (min)</label>
                <input type="number" id="work-duration" value="25" min="1" max="60">
            </div>
            <div class="setting-item">
                <label>Pause courte (min)</label>
                <input type="number" id="short-break" value="5" min="1" max="30">
            </div>
            <div class="setting-item">
                <label>Pause longue (min)</label>
                <input type="number" id="long-break" value="15" min="1" max="60">
            </div>
        </div>

        <div class="pomodoro-count">
            Pomodoros completes : <span id="pomodoro-count">0</span>
        </div>
    </div>
</div>
```

### Etape 6 : Creer l'onglet "Conseils"

```html
<div class="tab-content" id="tab-conseils">
    <div class="conseils-section">
        <h2>Conseils TDAH</h2>

        <!-- Filtres par categorie -->
        <div class="conseils-categories">
            <button class="category-btn active" data-category="tous">Tous</button>
            <button class="category-btn" data-category="concentration">Concentration</button>
            <button class="category-btn" data-category="organisation">Organisation</button>
            <button class="category-btn" data-category="motivation">Motivation</button>
            <button class="category-btn" data-category="gestion-stress">Gestion du stress</button>
        </div>

        <!-- Conseils pre-enregistres -->
        <div id="conseils-container">
            <div class="conseil-card" data-category="concentration">
                <h3>La regle des 2 minutes</h3>
                <p>Si une tache prend moins de 2 minutes, fais-la immediatement.</p>
            </div>
            <!-- Ajouter d'autres conseils... -->
        </div>

        <button class="btn-new-conseil" id="btn-new-conseil">Obtenir un conseil personnalise (IA)</button>
        <div id="conseil-ia" style="margin-top: 20px;"></div>
    </div>
</div>
```

### Etape 7 : Creer l'onglet "A connaitre"

```html
<div class="tab-content" id="tab-connaitre">
    <div class="connaitre-section">
        <h2>Fiches de revision personnalisees</h2>

        <div class="input-section" style="margin-bottom: 20px;">
            <label for="revision-input">Quel sujet veux-tu reviser ?</label>
            <textarea id="revision-input" placeholder="Ex: La Revolution francaise, Les equations du second degre..."></textarea>

            <!-- Selecteur de niveau -->
            <div style="margin-top: 15px;">
                <label for="niveau-select" style="display: block; margin-bottom: 8px;">Ton niveau scolaire :</label>
                <select id="niveau-select" class="niveau-select">
                    <option value="college">College (6e - 3e)</option>
                    <option value="seconde">Seconde</option>
                    <option value="premiere">Premiere</option>
                    <option value="terminale">Terminale</option>
                    <option value="bts" selected>BTS / DUT</option>
                    <option value="licence">Licence / Prepa</option>
                </select>
            </div>

            <button class="btn btn-primary" id="btn-generate-fiche" style="margin-top: 15px;">Generer ma fiche de revision</button>
        </div>

        <!-- Zone de chargement -->
        <div id="fiche-loading" class="loading" style="display: none;">
            <div class="loading-spinner"></div>
            <p>Generation de ta fiche personnalisee...</p>
        </div>

        <!-- Contenu de la fiche generee -->
        <div id="fiche-content" style="display: none;">
            <div id="fiche-dates" class="frise-container" style="display: none;">
                <h3 class="frise-title">&#128197; Dates importantes</h3>
                <div class="frise" id="frise-list"></div>
            </div>

            <div id="fiche-definitions" class="definitions-container" style="display: none;">
                <h3 class="frise-title">&#128213; Definitions cles</h3>
                <div id="definitions-list"></div>
            </div>

            <div id="fiche-formules" class="formules-container" style="display: none;">
                <h3 class="frise-title">&#128290; Formules essentielles</h3>
                <div id="formules-list"></div>
            </div>

            <div id="fiche-points" class="definitions-container" style="display: none;">
                <h3 class="frise-title">&#128161; Points cles a retenir</h3>
                <div id="points-list"></div>
            </div>
        </div>

        <div id="fiche-error" class="error" style="display: none;"></div>

        <!-- Historique -->
        <div id="fiches-historique" style="margin-top: 30px; display: none;">
            <h3 style="color: var(--text-secondary); margin-bottom: 15px;">Fiches precedentes</h3>
            <div id="historique-list" style="display: flex; flex-wrap: wrap; gap: 10px;"></div>
        </div>
    </div>
</div>
```

### Etape 8 : Ajouter le JavaScript pour la gestion du theme

```javascript
// =============================================
// GESTION DU THEME CLAIR/SOMBRE
// =============================================
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

function loadTheme() {
    const savedTheme = localStorage.getItem('tdah-theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    } else {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = prefersDark ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', theme);
        updateThemeIcon(theme);
    }
}

function updateThemeIcon(theme) {
    if (theme === 'light') {
        themeIcon.innerHTML = '&#9728;'; // Soleil
        themeToggle.title = 'Passer en mode sombre';
    } else {
        themeIcon.innerHTML = '&#9790;'; // Lune
        themeToggle.title = 'Passer en mode clair';
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('tdah-theme', newTheme);
    updateThemeIcon(newTheme);
}

themeToggle.addEventListener('click', toggleTheme);
loadTheme();
```

### Etape 9 : Ajouter le JavaScript pour la navigation par onglets

```javascript
// =============================================
// NAVIGATION PAR ONGLETS
// =============================================
const navTabs = document.querySelectorAll('.nav-tab');
const tabContents = document.querySelectorAll('.tab-content');

navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;

        // Desactiver tous les onglets
        navTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Cacher tous les contenus et afficher le bon
        tabContents.forEach(content => {
            content.classList.remove('active');
            if (content.id === `tab-${targetTab}`) {
                content.classList.add('active');
            }
        });
    });
});
```

### Etape 10 : Ajouter le JavaScript pour la decomposition de taches

```javascript
// =============================================
// DECOMPOSITION DE TACHES
// =============================================
const SPICINESS_CONFIG = {
    1: { label: "Minimaliste", emoji: "", description: "3-4 grandes etapes" },
    2: { label: "Simplifie", emoji: "", description: "4-6 etapes principales" },
    3: { label: "Equilibre", emoji: "", description: "6-8 etapes detaillees" },
    4: { label: "Detaille", emoji: "", description: "8-10 micro-etapes" },
    5: { label: "Ultra-detaille", emoji: "", description: "10-12 mini-etapes" }
};

const spicinessSlider = document.getElementById('spiciness-slider');
const spicinessValue = document.getElementById('spiciness-value');
const spicinessDisplay = document.getElementById('spiciness-display');
const taskInput = document.getElementById('task-input');
const decomposeBtn = document.getElementById('decompose-btn');
const resultsSection = document.getElementById('results-section');
const loading = document.getElementById('loading');
const resultsContent = document.getElementById('results-content');
const taskList = document.getElementById('task-list');
const errorMessage = document.getElementById('error-message');

let tasks = [];

// Mise a jour du slider
spicinessSlider.addEventListener('input', () => {
    const value = spicinessSlider.value;
    spicinessValue.textContent = value;
    const config = SPICINESS_CONFIG[value];
    spicinessDisplay.textContent = `${config.emoji} ${config.label} - ${config.description}`;
});

// Decomposition avec l'IA
decomposeBtn.addEventListener('click', async () => {
    const task = taskInput.value.trim();
    if (!task) {
        alert('Decris ta tache avant de la decomposer !');
        return;
    }

    resultsSection.classList.add('visible');
    loading.style.display = 'block';
    resultsContent.style.display = 'none';
    errorMessage.style.display = 'none';
    decomposeBtn.disabled = true;

    try {
        const spiciness = parseInt(spicinessSlider.value);
        const config = SPICINESS_CONFIG[spiciness];

        const prompt = `Tu es un expert en decomposition de taches pour personnes TDAH.

NIVEAU DE DETAIL : ${config.label} (${config.description})

TACHE A DECOMPOSER :
"${task}"

REGLES ABSOLUES :
1. Entre ${spiciness + 2} et ${spiciness + 7} etapes maximum
2. UN verbe d'action au debut de chaque etape
3. Phrases courtes (10 mots max)
4. Ordre logique progressif
5. Adapte au niveau scolaire francais

REPONDS UNIQUEMENT avec la liste numerotee, rien d'autre :
1. [ACTION]
2. [ACTION]
...`;

        const response = await puter.ai.chat(prompt);

        // Extraire le texte de la reponse
        let text = '';
        if (typeof response === 'string') {
            text = response;
        } else if (response?.message?.content) {
            text = response.message.content;
        }

        // Parser la reponse
        tasks = parseResponse(text);
        displayTasks(tasks);

        loading.style.display = 'none';
        resultsContent.style.display = 'block';

    } catch (error) {
        console.error('Erreur:', error);
        loading.style.display = 'none';
        errorMessage.textContent = `Erreur: ${error.message}`;
        errorMessage.style.display = 'block';
    }

    decomposeBtn.disabled = false;
});

function parseResponse(text) {
    const lines = text.split('\n')
        .map(line => line.trim())
        .filter(line => /^\d+\./.test(line))
        .map(line => line.replace(/^\d+\.\s*/, ''));

    return lines.map((title, index) => ({
        id: index + 1,
        title: title,
        completed: false
    }));
}

function displayTasks(tasks) {
    taskList.innerHTML = '';

    tasks.forEach((task, index) => {
        const li = document.createElement('li');
        li.className = 'task-item' + (task.completed ? ' completed' : '');
        li.innerHTML = `
            <div class="task-number">${index + 1}</div>
            <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} data-index="${index}">
            <div class="task-content">
                <div class="task-title">${task.title}</div>
            </div>
        `;
        taskList.appendChild(li);
    });

    // Ajouter les evenements checkbox
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const index = parseInt(e.target.dataset.index);
            tasks[index].completed = e.target.checked;
            e.target.closest('.task-item').classList.toggle('completed', e.target.checked);
            updateStats();
        });
    });

    updateStats();
}

function updateStats() {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((completed / total) * 100) : 0;

    document.getElementById('total-tasks').textContent = total;
    document.getElementById('completed-tasks').textContent = completed;
    document.getElementById('progress').textContent = progress + '%';
    document.getElementById('task-count').textContent = `${completed}/${total} terminees`;
}
```

### Etape 11 : Ajouter le JavaScript pour le Pomodoro

```javascript
// =============================================
// MINUTEUR POMODORO
// =============================================
let pomodoroInterval = null;
let pomodoroTimeLeft = 25 * 60;
let pomodoroIsRunning = false;
let pomodoroMode = 'work';
let pomodoroCount = 0;

const timerDisplay = document.getElementById('timer-display');
const timerStatus = document.getElementById('timer-status');
const btnStart = document.getElementById('btn-start');
const btnPause = document.getElementById('btn-pause');
const btnReset = document.getElementById('btn-reset');
const workDurationInput = document.getElementById('work-duration');
const shortBreakInput = document.getElementById('short-break');
const longBreakInput = document.getElementById('long-break');
const pomodoroCountDisplay = document.getElementById('pomodoro-count');

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function updateTimerDisplay() {
    timerDisplay.textContent = formatTime(pomodoroTimeLeft);
}

function playNotificationSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.value = 800;
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    } catch (e) {
        console.log('Son non disponible');
    }
}

function startPomodoro() {
    pomodoroIsRunning = true;
    btnStart.style.display = 'none';
    btnPause.style.display = 'inline-block';

    pomodoroInterval = setInterval(() => {
        pomodoroTimeLeft--;
        updateTimerDisplay();

        if (pomodoroTimeLeft <= 0) {
            clearInterval(pomodoroInterval);
            playNotificationSound();

            if (pomodoroMode === 'work') {
                pomodoroCount++;
                pomodoroCountDisplay.textContent = pomodoroCount;

                // Pause longue tous les 4 pomodoros
                if (pomodoroCount % 4 === 0) {
                    pomodoroMode = 'longBreak';
                    pomodoroTimeLeft = parseInt(longBreakInput.value) * 60;
                    timerStatus.textContent = 'Pause longue - Tu l\'as bien merite !';
                    timerStatus.className = 'timer-status break';
                } else {
                    pomodoroMode = 'shortBreak';
                    pomodoroTimeLeft = parseInt(shortBreakInput.value) * 60;
                    timerStatus.textContent = 'Pause courte - Detends-toi !';
                    timerStatus.className = 'timer-status break';
                }
            } else {
                pomodoroMode = 'work';
                pomodoroTimeLeft = parseInt(workDurationInput.value) * 60;
                timerStatus.textContent = 'Temps de travail - Concentre-toi !';
                timerStatus.className = 'timer-status work';
            }

            updateTimerDisplay();
            pomodoroIsRunning = false;
            btnStart.style.display = 'inline-block';
            btnPause.style.display = 'none';

            // Notification navigateur
            if (Notification.permission === 'granted') {
                new Notification('Pomodoro', {
                    body: pomodoroMode === 'work' ? 'C\'est l\'heure de travailler !' : 'Pause terminee !',
                });
            }
        }
    }, 1000);
}

function pausePomodoro() {
    pomodoroIsRunning = false;
    clearInterval(pomodoroInterval);
    btnStart.style.display = 'inline-block';
    btnPause.style.display = 'none';
    timerStatus.textContent = 'En pause';
}

function resetPomodoro() {
    clearInterval(pomodoroInterval);
    pomodoroIsRunning = false;
    pomodoroMode = 'work';
    pomodoroTimeLeft = parseInt(workDurationInput.value) * 60;
    updateTimerDisplay();
    btnStart.style.display = 'inline-block';
    btnPause.style.display = 'none';
    timerStatus.textContent = 'Pret a travailler';
    timerStatus.className = 'timer-status';
}

btnStart.addEventListener('click', startPomodoro);
btnPause.addEventListener('click', pausePomodoro);
btnReset.addEventListener('click', resetPomodoro);

// Demander la permission pour les notifications
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}
```

### Etape 12 : Ajouter le JavaScript pour les fiches de revision

```javascript
// =============================================
// SECTION A CONNAITRE - FICHES DYNAMIQUES
// =============================================
const revisionInput = document.getElementById('revision-input');
const niveauSelect = document.getElementById('niveau-select');
const btnGenerateFiche = document.getElementById('btn-generate-fiche');
const ficheLoading = document.getElementById('fiche-loading');
const ficheContent = document.getElementById('fiche-content');
const ficheError = document.getElementById('fiche-error');
const fichesHistorique = document.getElementById('fiches-historique');
const historiqueList = document.getElementById('historique-list');

// Elements pour afficher le contenu
const ficheDates = document.getElementById('fiche-dates');
const ficheDefinitions = document.getElementById('fiche-definitions');
const ficheFormules = document.getElementById('fiche-formules');
const fichePoints = document.getElementById('fiche-points');
const friseList = document.getElementById('frise-list');
const definitionsList = document.getElementById('definitions-list');
const formulesList = document.getElementById('formules-list');
const pointsList = document.getElementById('points-list');

// Sauvegarder le niveau choisi
const savedNiveau = localStorage.getItem('niveau-scolaire');
if (savedNiveau) {
    niveauSelect.value = savedNiveau;
}
niveauSelect.addEventListener('change', () => {
    localStorage.setItem('niveau-scolaire', niveauSelect.value);
});

// Historique des fiches
let fichesHistory = JSON.parse(localStorage.getItem('fiches-history') || '[]');

function updateHistoriqueDisplay() {
    if (fichesHistory.length === 0) {
        fichesHistorique.style.display = 'none';
        return;
    }

    fichesHistorique.style.display = 'block';
    historiqueList.innerHTML = '';

    fichesHistory.slice(-5).reverse().forEach((fiche) => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = fiche.sujet.substring(0, 25) + (fiche.sujet.length > 25 ? '...' : '');
        btn.title = fiche.sujet;
        btn.addEventListener('click', () => {
            displayFicheData(fiche.data);
            ficheContent.style.display = 'block';
        });
        historiqueList.appendChild(btn);
    });
}

updateHistoriqueDisplay();

function displayFicheData(data) {
    // Reset toutes les sections
    ficheDates.style.display = 'none';
    ficheDefinitions.style.display = 'none';
    ficheFormules.style.display = 'none';
    fichePoints.style.display = 'none';
    friseList.innerHTML = '';
    definitionsList.innerHTML = '';
    formulesList.innerHTML = '';
    pointsList.innerHTML = '';

    // Afficher les dates si presentes
    if (data.dates && data.dates.length > 0) {
        ficheDates.style.display = 'block';
        data.dates.forEach(item => {
            const div = document.createElement('div');
            div.className = 'frise-item';
            div.innerHTML = `
                <div class="frise-date">${item.date}</div>
                <div class="frise-event">${item.evenement}</div>
                ${item.detail ? `<div class="frise-detail">${item.detail}</div>` : ''}
            `;
            friseList.appendChild(div);
        });
    }

    // Afficher les definitions si presentes
    if (data.definitions && data.definitions.length > 0) {
        ficheDefinitions.style.display = 'block';
        data.definitions.forEach(item => {
            const div = document.createElement('div');
            div.className = 'definition-card';
            div.innerHTML = `
                <div class="definition-term">${item.terme}</div>
                <div class="definition-text">${item.definition}</div>
            `;
            definitionsList.appendChild(div);
        });
    }

    // Afficher les formules si presentes
    if (data.formules && data.formules.length > 0) {
        ficheFormules.style.display = 'block';
        data.formules.forEach(item => {
            const div = document.createElement('div');
            div.className = 'formule-card';
            div.innerHTML = `
                <div class="formule-name">${item.nom}</div>
                <div class="formule-expression">${item.formule}</div>
                ${item.description ? `<div class="formule-description">${item.description}</div>` : ''}
            `;
            formulesList.appendChild(div);
        });
    }

    // Afficher les points cles si presents
    if (data.points && data.points.length > 0) {
        fichePoints.style.display = 'block';
        data.points.forEach(item => {
            const div = document.createElement('div');
            div.className = 'definition-card';
            div.style.borderLeftColor = '#667eea';
            div.innerHTML = `
                <div class="definition-term" style="color: #667eea;">${item.titre}</div>
                <div class="definition-text">${item.contenu}</div>
            `;
            pointsList.appendChild(div);
        });
    }
}

btnGenerateFiche.addEventListener('click', async () => {
    const sujet = revisionInput.value.trim();
    if (!sujet) {
        alert('Indique le sujet que tu veux reviser !');
        return;
    }

    ficheLoading.style.display = 'block';
    ficheContent.style.display = 'none';
    ficheError.style.display = 'none';
    btnGenerateFiche.disabled = true;

    try {
        const niveau = niveauSelect.value;
        const niveauLabels = {
            'college': 'College (6e-3e) - vocabulaire simple, concepts de base',
            'seconde': 'Seconde - notions intermediaires, debut de specialisation',
            'premiere': 'Premiere - notions avancees, preparation au bac',
            'terminale': 'Terminale - niveau bac, concepts approfondis',
            'bts': 'BTS/DUT - niveau post-bac, applications professionnelles',
            'licence': 'Licence/Prepa - niveau universitaire, rigueur scientifique'
        };

        const prompt = `Tu es un assistant pedagogique expert.

SUJET A REVISER : "${sujet}"
NIVEAU SCOLAIRE : ${niveauLabels[niveau]}

Genere une fiche de revision ADAPTEE au sujet ET au niveau demande.

REPONDS UNIQUEMENT en JSON valide. Utilise UNIQUEMENT les sections pertinentes :

{
  "dates": [
    {"date": "1789", "evenement": "Revolution francaise", "detail": "Prise de la Bastille"}
  ],
  "definitions": [
    {"terme": "Terme", "definition": "Explication claire"}
  ],
  "formules": [
    {"nom": "Nom", "formule": "E = mc²", "description": "Explication"}
  ],
  "points": [
    {"titre": "Point important", "contenu": "A retenir"}
  ]
}

REGLES STRICTES :
- ADAPTE LA COMPLEXITE AU NIVEAU : vocabulaire, profondeur des explications, difficulte des formules
- "dates" : UNIQUEMENT si le sujet est de l'HISTOIRE ou des EVENEMENTS HISTORIQUES. PAS pour maths, sciences, info, langues.
- "formules" : UNIQUEMENT pour maths, physique, chimie, economie. PAS pour histoire, francais, langues.
- "definitions" : TOUJOURS inclure (adapte au niveau)
- "points" : TOUJOURS inclure (adapte au niveau)
- Si une section n'est pas pertinente au SUJET, NE PAS l'inclure
- Maximum 6 elements par section
- JSON uniquement, sans texte avant ou apres`;

        const response = await puter.ai.chat(prompt);

        let text = '';
        if (typeof response === 'string') {
            text = response;
        } else if (response?.message?.content) {
            text = response.message.content;
        }

        // Nettoyer le texte pour extraire le JSON
        text = text.trim();
        if (text.startsWith('```json')) {
            text = text.replace(/^```json\n?/, '').replace(/\n?```$/, '');
        } else if (text.startsWith('```')) {
            text = text.replace(/^```\n?/, '').replace(/\n?```$/, '');
        }

        const data = JSON.parse(text);

        // Afficher les donnees
        displayFicheData(data);
        ficheContent.style.display = 'block';

        // Sauvegarder dans l'historique
        fichesHistory.push({
            sujet: sujet,
            data: data,
            date: new Date().toISOString()
        });
        if (fichesHistory.length > 10) {
            fichesHistory = fichesHistory.slice(-10);
        }
        localStorage.setItem('fiches-history', JSON.stringify(fichesHistory));
        updateHistoriqueDisplay();

    } catch (error) {
        console.error('Erreur:', error);
        ficheError.textContent = `Erreur lors de la generation : ${error.message}`;
        ficheError.style.display = 'block';
    }

    ficheLoading.style.display = 'none';
    btnGenerateFiche.disabled = false;
});
```

---

## 5. Fonctionnalites detaillees

### 5.1 Decomposition de taches

**Principe** : L'utilisateur decrit une tache complexe, choisit un niveau de detail (1-5), et l'IA decompose la tache en sous-etapes.

**Niveaux de detail** :
| Niveau | Label | Description |
|--------|-------|-------------|
| 1 | Minimaliste | 3-4 grandes etapes |
| 2 | Simplifie | 4-6 etapes principales |
| 3 | Equilibre | 6-8 etapes detaillees |
| 4 | Detaille | 8-10 micro-etapes |
| 5 | Ultra-detaille | 10-12 mini-etapes |

**Fonctionnalites** :
- Checkbox pour marquer les taches terminees
- Statistiques en temps reel (total, terminees, progression)
- Animation visuelle des taches completees
- **Systeme de felicitations** quand toutes les taches sont cochees

### 5.2 Systeme de felicitations

**Declenchement** : Quand toutes les checkboxes sont cochees (100% de progression)

**Elements visuels** :
- **Confettis animes** : 50 confettis colores tombent du haut de l'ecran
- **Popup de felicitations** avec :
  - Emoji anime (rebondit)
  - Message aleatoire parmi 5 possibilites
  - Bouton "Continuer" pour fermer

**Messages aleatoires** :
| Emoji | Titre | Message |
|-------|-------|---------|
| 🎉 | Bravo ! | Tu as termine toutes tes taches ! |
| 🏆 | Champion ! | Toutes les etapes sont completees ! |
| ⭐ | Excellent ! | Mission accomplie avec succes ! |
| 🚀 | Incroyable ! | Tu as tout dechire ! |
| 💪 | Super travail ! | Tu peux etre fier de toi ! |

**Son de victoire** : Melodie Do-Mi-Sol-Do (accord majeur ascendant)

**Code JavaScript** :
```javascript
function showCelebration() {
    createConfetti();

    const messages = [
        { emoji: '🎉', title: 'Bravo !', message: 'Tu as termine toutes tes taches !' },
        // ... autres messages
    ];

    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    // Afficher l'overlay avec le message
}

function createConfetti() {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            document.body.appendChild(confetti);
        }, i * 50);
    }
}
```

**CSS pour les confettis** :
```css
.confetti {
    position: fixed;
    width: 10px;
    height: 10px;
    top: -10px;
    z-index: 1001;
    animation: fall linear forwards;
}

@keyframes fall {
    to {
        transform: translateY(100vh) rotate(720deg);
    }
}

.celebration-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
```

### 5.3 Minuteur Pomodoro

**Technique Pomodoro** :
1. Travail pendant 25 minutes
2. Pause courte de 5 minutes
3. Apres 4 pomodoros : pause longue de 15 minutes

**Fonctionnalites** :
- Durees configurables
- Notification sonore a la fin de chaque periode
- Notification navigateur (si autorisee)
- Compteur de pomodoros completes
- Statut visuel (travail = vert, pause = orange)

### 5.4 Conseils TDAH

**Categories** :
- Tous
- Concentration
- Organisation
- Motivation
- Gestion du stress

**Fonctionnalites** :
- Conseils pre-enregistres filtrable par categorie
- Generation de conseils personnalises via IA

### 5.5 Fiches de revision

**Sections generees dynamiquement** :
- **Dates** : Frise chronologique (uniquement pour l'histoire)
- **Definitions** : Termes cles du sujet
- **Formules** : Equations et formules (maths, physique, chimie)
- **Points cles** : Informations importantes a retenir

**Niveaux scolaires** :
- College (6e - 3e)
- Seconde
- Premiere
- Terminale
- BTS / DUT
- Licence / Prepa

**Fonctionnalites** :
- Adaptation du contenu au niveau scolaire
- Historique des 5 dernieres fiches
- Sauvegarde dans localStorage
- **Systeme de feedback** integre pour ameliorer les generations futures

### 5.6 Systeme de feedback (Fiches de revision)

**Objectif** : Collecter les retours utilisateur pour ameliorer les prochaines fiches generees par l'IA.

**Elements de feedback** :

1. **Notation par etoiles (1-5)**
   - Hover : apercu de la note
   - Clic : validation de la note
   - Animation doree avec effet brillant

2. **Tags de feedback** (selection multiple) :
   | Tag | Description |
   |-----|-------------|
   | Trop simple | Le contenu manque de profondeur |
   | Trop complexe | Le vocabulaire est trop avance |
   | Manque d'exemples | Besoin d'illustrations concretes |
   | Manque de details | Explications trop succinctes |
   | Trop long | Contenu a condenser |
   | Trop court | Contenu a developper |
   | Formules incorrectes | Erreurs dans les equations |
   | Parfait ! | Aucune amelioration necessaire |

3. **Commentaire libre** (optionnel) : Zone de texte pour des retours detailles

**Stockage** : Les 50 derniers feedbacks sont sauvegardes dans `localStorage` sous la cle `fiches-feedback`.

**Utilisation dans le prompt IA** :
```javascript
function getFeedbackInstructions() {
    // Analyse les feedbacks precedents pour le niveau actuel
    const relevantFeedback = feedbackData.filter(f => f.niveau === niveau);

    // Compte les tags pour identifier les tendances
    const tagCounts = {};
    relevantFeedback.forEach(f => {
        f.tags.forEach(tag => {
            tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        });
    });

    // Genere des instructions basees sur les retours
    let instructions = '';
    if (tagCounts['trop-simple'] > tagCounts['trop-complexe']) {
        instructions += '- Augmente le niveau de difficulte\n';
    }
    if (tagCounts['manque-exemples'] >= 1) {
        instructions += '- AJOUTE DES EXEMPLES CONCRETS\n';
    }
    // ... autres regles

    return instructions;
}
```

**Regles d'amelioration automatique** :
- Si "trop simple" > "trop complexe" → Augmenter la difficulte
- Si "trop complexe" > "trop simple" → Simplifier le vocabulaire
- Si "manque d'exemples" ≥ 1 → Ajouter des exemples concrets
- Si "manque de details" ≥ 1 → Developper les explications
- Si note moyenne < 3 → Ameliorer significativement la qualite
- Les 3 derniers commentaires pertinents sont transmis a l'IA

### 5.7 Systeme de traduction FR/EN

**Objectif** : Permettre aux utilisateurs francophones et anglophones d'utiliser l'application dans leur langue preferee.

**Bouton de langue** :
- Position : en haut a droite, a cote du bouton de theme
- Affiche "EN" quand le site est en francais (pour passer en anglais)
- Affiche "FR" quand le site est en anglais (pour passer en francais)
- Sauvegarde la preference dans localStorage

**Elements traduits** :
| Section | Elements |
|---------|----------|
| Header | Titre, sous-titre |
| Navigation | Onglets (Taches/Tasks, Pomodoro, Conseils/Tips, A connaitre/Study Cards) |
| Taches | Labels, placeholders, boutons, statistiques |
| Pomodoro | Statuts, boutons, labels des parametres, notifications |
| Conseils | Titre, categories, 10 conseils complets |
| Fiches | Labels, niveaux scolaires, sections, feedback |
| Alertes | Messages d'erreur et de validation |

**Structure du dictionnaire de traductions** :
```javascript
const translations = {
    fr: {
        'title': 'Assistant TDAH Intelligent',
        'subtitle': 'Decompose tes taches, gere ton temps...',
        'tab-taches': 'Taches',
        'tab-pomodoro': 'Pomodoro',
        // ... toutes les traductions FR
    },
    en: {
        'title': 'Smart ADHD Assistant',
        'subtitle': 'Break down your tasks, manage your time...',
        'tab-taches': 'Tasks',
        'tab-pomodoro': 'Pomodoro',
        // ... toutes les traductions EN
    }
};
```

**Fonctions principales** :
```javascript
function loadLang() {
    const savedLang = localStorage.getItem('tdah-lang') || 'fr';
    currentLang = savedLang;
    applyTranslations(savedLang);
    updateLangIcon(savedLang);
}

function toggleLang() {
    currentLang = currentLang === 'fr' ? 'en' : 'fr';
    localStorage.setItem('tdah-lang', currentLang);
    applyTranslations(currentLang);
    updateLangIcon(currentLang);
}

function applyTranslations(lang) {
    const t = translations[lang];
    // Applique toutes les traductions aux elements DOM
    document.querySelector('header h1').textContent = t['title'];
    // ... autres elements
}
```

**CSS pour le bouton de langue** :
```css
.lang-toggle {
    position: fixed;
    top: 20px;
    right: 80px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    font-size: 16px;
    font-weight: bold;
}
```

**CSS pour le feedback** :
```css
.feedback-section {
    background: var(--bg-tertiary);
    border-radius: 10px;
    padding: 20px;
    margin-top: 25px;
    border: 2px dashed var(--accent-primary);
}

.star-btn {
    background: none;
    border: none;
    font-size: 28px;
    cursor: pointer;
    color: var(--text-muted);
    transition: all 0.2s;
}

.star-btn:hover, .star-btn.active {
    color: #FFD700;
    transform: scale(1.2);
}

.feedback-tag {
    padding: 8px 14px;
    border: 2px solid var(--border-color);
    background: transparent;
    border-radius: 20px;
    cursor: pointer;
}

.feedback-tag.active {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: #fff;
}
```

---

## 6. Code CSS complet

Le CSS complet est disponible dans le fichier source. Points cles :

### Variables CSS pour les themes
```css
:root { /* Mode sombre */ }
[data-theme="light"] { /* Mode clair */ }
```

### Classes principales
- `.container` : Conteneur principal (max-width: 800px)
- `.input-section` : Sections de saisie
- `.results-section` : Affichage des resultats
- `.task-item` : Elements de liste de taches
- `.pomodoro-section` : Section timer
- `.conseil-card` : Cartes de conseils
- `.frise-item` : Elements de frise chronologique
- `.definition-card` : Cartes de definitions
- `.formule-card` : Cartes de formules
- `.feedback-section` : Section de feedback
- `.star-btn` : Boutons etoiles pour notation
- `.feedback-tag` : Tags de feedback cliquables
- `.celebration-overlay` : Overlay de felicitations
- `.confetti` : Elements confettis animes
- `.niveau-select` : Selecteur de niveau scolaire stylise
- `.lang-toggle` : Bouton de basculement de langue FR/EN
- `.theme-toggle` : Bouton de basculement theme clair/sombre

### Animations
- `.loading-spinner` : Animation de chargement (rotation)
- `@keyframes fadeIn` : Apparition progressive
- `@keyframes bounceIn` : Apparition avec rebond
- `@keyframes bounce` : Rebond continu (emoji)
- `@keyframes fall` : Chute des confettis
- Transitions sur les hover (0.3s ease)

---

## 7. Code JavaScript complet

Le JavaScript est organise en sections :

1. **Gestion du theme** : Chargement, basculement, sauvegarde
2. **Navigation** : Onglets, affichage/masquage du contenu
3. **Decomposition de taches** : Appel API, parsing, affichage
4. **Systeme de felicitations** : Confettis, overlay, son de victoire
5. **Pomodoro** : Timer, notifications, configuration
6. **Conseils** : Filtrage, generation IA
7. **Fiches de revision** : Generation, affichage, historique
8. **Systeme de feedback** : Notation, tags, commentaires, analyse pour prompt IA

### Fonctions principales ajoutees

```javascript
// Felicitations
function showCelebration() { /* Affiche popup + confettis */ }
function closeCelebration() { /* Ferme et nettoie */ }
function createConfetti() { /* Cree 50 confettis animes */ }
function playCelebrationSound() { /* Melodie Do-Mi-Sol-Do */ }

// Feedback
function getFeedbackInstructions() { /* Analyse feedbacks → instructions IA */ }
function updateStarsDisplay() { /* Met a jour affichage etoiles */ }
function resetFeedbackForm() { /* Reinitialise le formulaire */ }
```

---

## 8. Personnalisation

### Changer les couleurs
Modifier les variables CSS dans `:root` et `[data-theme="light"]` :
```css
--accent-primary: #667eea;  /* Couleur principale */
--accent-secondary: #764ba2; /* Couleur secondaire */
```

### Ajouter des conseils
Dans le HTML, ajouter des cartes dans `#conseils-container` :
```html
<div class="conseil-card" data-category="concentration">
    <h3>Titre du conseil</h3>
    <p>Description du conseil...</p>
</div>
```

### Modifier les niveaux scolaires
Dans le HTML, modifier les `<option>` du select `#niveau-select` et adapter le JavaScript dans `niveauLabels`.

### Changer les durees Pomodoro par defaut
Modifier les attributs `value` des inputs :
```html
<input type="number" id="work-duration" value="25">
<input type="number" id="short-break" value="5">
<input type="number" id="long-break" value="15">
```

### Personnaliser les messages de felicitations
Modifier le tableau `messages` dans la fonction `showCelebration()` :
```javascript
const messages = [
    { emoji: '🎉', title: 'Bravo !', message: 'Tu as termine toutes tes taches !' },
    { emoji: '🏆', title: 'Champion !', message: 'Toutes les etapes sont completees !' },
    // Ajouter vos propres messages ici
];
```

### Personnaliser les tags de feedback
Dans le HTML, modifier les boutons dans `.feedback-tags` :
```html
<div class="feedback-tags" id="feedback-tags">
    <button class="feedback-tag" data-tag="mon-tag">Mon tag personnalise</button>
    <!-- Ajouter d'autres tags -->
</div>
```

Puis adapter la fonction `getFeedbackInstructions()` pour gerer les nouveaux tags.

### Modifier le son de victoire
Dans `playCelebrationSound()`, modifier le tableau `notes` (frequences en Hz) :
```javascript
const notes = [523.25, 659.25, 783.99, 1046.50]; // Do Mi Sol Do
// Exemples d'autres notes :
// La (440), Si (493.88), Do (523.25), Re (587.33), Mi (659.25)
```

### Desactiver les felicitations
Supprimer ou commenter l'appel a `showCelebration()` dans `updateStats()` :
```javascript
if (total > 0 && completed === total && !hasShownCelebration) {
    hasShownCelebration = true;
    // showCelebration(); // Desactive
}
```

---

## Conclusion

Ce projet est une application web complete qui utilise :
- **HTML/CSS/JS** pour l'interface
- **Puter.js** pour l'intelligence artificielle (gratuit, sans cle API)
- **localStorage** pour la persistance des donnees

### Fonctionnalites implementees

| Fonctionnalite | Description |
|----------------|-------------|
| Decomposition de taches | IA decompose les taches complexes en etapes |
| Felicitations | Confettis + popup quand tout est coche |
| Pomodoro | Timer configurable avec notifications |
| Conseils TDAH | Conseils filtres + generation IA |
| Fiches de revision | Generees par IA, adaptees au niveau |
| Feedback | Notation + tags pour ameliorer l'IA |
| Theme clair/sombre | Basculement manuel ou automatique |
| Traduction FR/EN | Interface bilingue avec sauvegarde de preference |

### Donnees sauvegardees (localStorage)

| Cle | Contenu |
|-----|---------|
| `tdah-theme` | Theme actuel (dark/light) |
| `tdah-lang` | Langue actuelle (fr/en) |
| `niveau-scolaire` | Niveau scolaire selectionne |
| `fiches-history` | 10 dernieres fiches generees |
| `fiches-feedback` | 50 derniers feedbacks |

L'application est entierement contenue dans un seul fichier HTML, ce qui la rend facile a deployer et a partager.

Pour l'utiliser, il suffit d'ouvrir le fichier `assistant_tdah.html` dans un navigateur moderne. Une popup de connexion Puter apparaitra lors de la premiere utilisation d'une fonctionnalite IA.

---

*Documentation mise a jour le 22 janvier 2026*
