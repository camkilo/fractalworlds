/**
 * Fractal Worlds RPG - Main Game Logic
 * Handles API communication, game state, and core game loop
 */

class FractalWorldsGame {
    constructor() {
        this.sessionId = null;
        this.playerData = null;
        this.worldData = null;
        this.gameState = 'loading';
        this.updateInterval = null;
        this.moveQueue = [];
        this.isMoving = false;
        
        // Configuration constants
        this.UPDATE_INTERVAL_MS = 2000; // Update game state every 2 seconds
        
        // Load saved session if exists
        const savedSession = localStorage.getItem('fw_session');
        if (savedSession) {
            this.sessionId = savedSession;
        }
    }

    /**
     * Initialize the game
     */
    async init() {
        console.log('Initializing Fractal Worlds RPG...');
        
        // Show new game screen after brief loading
        setTimeout(() => {
            this.showScreen('newGameScreen');
        }, 1000);
    }

    /**
     * Start a new game
     */
    async startNewGame(playerName, seed, difficulty) {
        try {
            this.showScreen('loadingScreen');
            const loadingText = document.querySelector('#loadingScreen .subtitle');
            loadingText.textContent = 'Generating fractal world...';

            console.log('Starting new game:', { playerName, seed, difficulty });

            const response = await fetch('/api/game/new', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_name: playerName,
                    seed: parseInt(seed),
                    difficulty: difficulty
                })
            });

            const data = await response.json();

            if (data.success) {
                this.sessionId = data.session_id;
                localStorage.setItem('fw_session', this.sessionId);
                
                loadingText.textContent = 'Loading player data...';
                await this.loadGameState();
                
                loadingText.textContent = 'Initializing game world...';
                await this.startGameLoop();
                
                this.showScreen('gameScreen');
                this.gameState = 'playing';
                
                UI.showMessage('Welcome to Fractal Worlds, ' + playerName + '!', 'success');
            } else {
                throw new Error(data.message || 'Failed to start game');
            }
        } catch (error) {
            console.error('Error starting game:', error);
            UI.showMessage('Failed to start game: ' + error.message, 'error');
            this.showScreen('newGameScreen');
        }
    }

    /**
     * Load current game state from server
     */
    async loadGameState() {
        try {
            const response = await fetch(`/api/game/${this.sessionId}/status`);
            const data = await response.json();

            if (data.success) {
                this.playerData = data.player;
                this.worldData = data.world || null;
                UI.updatePlayerUI(this.playerData);
                return true;
            } else {
                throw new Error('Failed to load game state');
            }
        } catch (error) {
            console.error('Error loading game state:', error);
            return false;
        }
    }

    /**
     * Start the game loop
     */
    async startGameLoop() {
        // Update game state at configured interval
        this.updateInterval = setInterval(async () => {
            if (this.gameState === 'playing') {
                await this.updateGame();
            }
        }, this.UPDATE_INTERVAL_MS);

        // Initial update
        await this.updateGame();
    }

    /**
     * Update game state
     */
    async updateGame() {
        const success = await this.loadGameState();
        if (success) {
            Renderer.render();
        }
    }

    /**
     * Move player
     */
    async movePlayer(direction) {
        if (this.isMoving || !this.sessionId) return;
        
        this.isMoving = true;
        
        try {
            const response = await fetch(`/api/game/${this.sessionId}/move`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ direction })
            });

            const data = await response.json();

            if (data.success) {
                this.playerData = data.player;
                UI.updatePlayerUI(this.playerData);
                Renderer.render();
                
                if (data.message) {
                    UI.showMessage(data.message, 'success');
                }

                // Check for encounters
                if (data.encounter) {
                    this.handleEncounter(data.encounter);
                }
            } else {
                UI.showMessage(data.message || 'Cannot move in that direction', 'warning');
            }
        } catch (error) {
            console.error('Error moving player:', error);
            UI.showMessage('Movement failed', 'error');
        } finally {
            this.isMoving = false;
        }
    }

    /**
     * Perform action (attack, gather, interact, etc.)
     */
    async performAction(action, params = {}) {
        if (!this.sessionId) return;

        try {
            const response = await fetch(`/api/game/${this.sessionId}/action`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action, ...params })
            });

            const data = await response.json();

            if (data.success) {
                if (data.player) {
                    this.playerData = data.player;
                    UI.updatePlayerUI(this.playerData);
                }
                
                if (data.message) {
                    UI.showMessage(data.message, 'success');
                }

                if (data.combat_result) {
                    this.handleCombatResult(data.combat_result);
                }

                Renderer.render();
            } else {
                UI.showMessage(data.message || 'Action failed', 'warning');
            }
        } catch (error) {
            console.error('Error performing action:', error);
            UI.showMessage('Action failed', 'error');
        }
    }

    /**
     * Handle encounter
     */
    handleEncounter(encounter) {
        console.log('Encounter:', encounter);
        UI.showCombat(encounter);
    }

    /**
     * Handle combat result
     */
    handleCombatResult(result) {
        console.log('Combat result:', result);
        
        if (result.player_victory) {
            UI.showMessage('Victory! ' + result.message, 'success');
            UI.hideCombat();
        } else if (result.enemy_victory) {
            UI.showMessage('Defeated! ' + result.message, 'error');
            UI.hideCombat();
        } else {
            UI.showMessage(result.message, 'warning');
        }
    }

    /**
     * Save game
     */
    async saveGame() {
        if (!this.sessionId) return;

        try {
            const response = await fetch(`/api/game/${this.sessionId}/save`, {
                method: 'POST'
            });

            const data = await response.json();

            if (data.success) {
                UI.showMessage('Game saved successfully!', 'success');
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Error saving game:', error);
            UI.showMessage('Failed to save game', 'error');
        }
    }

    /**
     * Show screen
     */
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }

    /**
     * Stop game loop
     */
    stopGameLoop() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
}

// Initialize game instance
const Game = new FractalWorldsGame();

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    Game.init();

    // New game screen buttons
    document.getElementById('startGameBtn').addEventListener('click', () => {
        const playerName = document.getElementById('playerName').value || 'Adventurer';
        const seed = document.getElementById('worldSeed').value || Math.floor(Math.random() * 1000000);
        const difficulty = document.getElementById('difficulty').value;
        Game.startNewGame(playerName, seed, difficulty);
    });

    document.getElementById('randomSeedBtn').addEventListener('click', () => {
        document.getElementById('worldSeed').value = Math.floor(Math.random() * 1000000);
    });

    document.getElementById('aboutBtn').addEventListener('click', () => {
        window.open('/landing.html', '_blank');
    });

    // Menu buttons
    document.getElementById('menuBtn').addEventListener('click', () => {
        UI.showMenu();
    });

    document.getElementById('resumeBtn').addEventListener('click', () => {
        UI.hideMenu();
    });

    document.getElementById('saveBtn').addEventListener('click', () => {
        Game.saveGame();
    });

    document.getElementById('aboutGameBtn').addEventListener('click', () => {
        window.open('/landing.html', '_blank');
    });

    document.getElementById('newGameFromMenuBtn').addEventListener('click', () => {
        if (confirm('Start a new game? Current progress will be lost.')) {
            Game.stopGameLoop();
            localStorage.removeItem('fw_session');
            location.reload();
        }
    });

    // Keyboard controls
    document.addEventListener('keydown', (e) => {
        if (Game.gameState !== 'playing') return;

        // Don't handle if user is typing in an input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        switch (e.key.toLowerCase()) {
            case 'w':
            case 'arrowup':
                Game.movePlayer('north');
                e.preventDefault();
                break;
            case 's':
            case 'arrowdown':
                Game.movePlayer('south');
                e.preventDefault();
                break;
            case 'a':
            case 'arrowleft':
                Game.movePlayer('west');
                e.preventDefault();
                break;
            case 'd':
            case 'arrowright':
                Game.movePlayer('east');
                e.preventDefault();
                break;
            case 'e':
                Game.performAction('gather');
                e.preventDefault();
                break;
            case ' ':
                Game.performAction('interact');
                e.preventDefault();
                break;
            case 'escape':
                UI.toggleMenu();
                e.preventDefault();
                break;
        }
    });

    // Combat action buttons
    document.querySelectorAll('.btn-action').forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            Game.performAction(action);
        });
    });

    // Initialize renderer
    Renderer.init();
});
