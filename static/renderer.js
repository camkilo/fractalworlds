/**
 * Fractal Worlds RPG - Renderer
 * Handles canvas rendering for game world, minimap, and visual effects
 */

const Renderer = {
    canvas: null,
    ctx: null,
    minimapCanvas: null,
    minimapCtx: null,
    cellSize: 32,
    viewportWidth: 15,
    viewportHeight: 15,
    
    /**
     * Initialize renderer
     */
    init() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        this.minimapCanvas = document.getElementById('minimapCanvas');
        this.minimapCtx = this.minimapCanvas.getContext('2d');
        
        // Set canvas size
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        // Initial render
        this.render();
    },

    /**
     * Resize canvas to fit container
     */
    resize() {
        const container = this.canvas.parentElement;
        const width = Math.floor(container.clientWidth * 0.95);
        const height = Math.floor(container.clientHeight * 0.95);
        
        // Calculate dimensions to maintain aspect ratio
        const cellCount = Math.min(this.viewportWidth, this.viewportHeight);
        const size = Math.min(width, height);
        
        this.canvas.width = this.viewportWidth * this.cellSize;
        this.canvas.height = this.viewportHeight * this.cellSize;
        
        // Apply CSS size
        this.canvas.style.width = size + 'px';
        this.canvas.style.height = size + 'px';
    },

    /**
     * Render game world
     */
    render() {
        if (!Game.playerData) {
            this.renderLoading();
            return;
        }

        this.renderWorld();
        this.renderMinimap();
    },

    /**
     * Render loading screen on canvas
     */
    renderLoading() {
        this.ctx.fillStyle = '#0f0f1e';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '24px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Loading...', this.canvas.width / 2, this.canvas.height / 2);
    },

    /**
     * Render game world
     */
    renderWorld() {
        const ctx = this.ctx;
        const cellSize = this.cellSize;
        
        // Clear canvas
        ctx.fillStyle = '#0f0f1e';
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Calculate viewport center on player
        const playerPos = Game.playerData.position;
        const centerX = Math.floor(this.viewportWidth / 2);
        const centerY = Math.floor(this.viewportHeight / 2);

        // Render grid
        for (let y = 0; y < this.viewportHeight; y++) {
            for (let x = 0; x < this.viewportWidth; x++) {
                const worldX = Math.floor(playerPos[0]) + (x - centerX);
                const worldY = Math.floor(playerPos[1]) + (y - centerY);
                
                // Draw cell
                this.drawCell(ctx, x, y, worldX, worldY, cellSize);
            }
        }

        // Draw player at center
        this.drawPlayer(ctx, centerX, centerY, cellSize);

        // Draw grid lines
        ctx.strokeStyle = 'rgba(102, 126, 234, 0.2)';
        ctx.lineWidth = 1;
        for (let x = 0; x <= this.viewportWidth; x++) {
            ctx.beginPath();
            ctx.moveTo(x * cellSize, 0);
            ctx.lineTo(x * cellSize, this.canvas.height);
            ctx.stroke();
        }
        for (let y = 0; y <= this.viewportHeight; y++) {
            ctx.beginPath();
            ctx.moveTo(0, y * cellSize);
            ctx.lineTo(this.canvas.width, y * cellSize);
            ctx.stroke();
        }
    },

    /**
     * Draw a single cell
     */
    drawCell(ctx, x, y, worldX, worldY, cellSize) {
        const px = x * cellSize;
        const py = y * cellSize;

        // Generate procedural terrain based on position
        const biome = this.getBiomeAtPosition(worldX, worldY);
        const color = this.getBiomeColor(biome);

        // Draw background
        ctx.fillStyle = color;
        ctx.fillRect(px, py, cellSize, cellSize);

        // Add some noise/variation
        const noise = (Math.sin(worldX * 0.1) + Math.cos(worldY * 0.1)) * 10;
        if (noise > 5) {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.fillRect(px, py, cellSize, cellSize);
        }

        // Random features (trees, rocks, etc.)
        if (this.hasFeature(worldX, worldY)) {
            const feature = this.getFeatureIcon(biome, worldX, worldY);
            ctx.font = `${cellSize * 0.7}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(feature, px + cellSize / 2, py + cellSize / 2);
        }
    },

    /**
     * Get biome at position (procedural)
     */
    getBiomeAtPosition(x, y) {
        // Simple procedural biome generation
        const hash = (x * 374761393 + y * 668265263) % 1000000;
        const val = (hash / 1000000);
        
        if (val < 0.1) return 'water';
        if (val < 0.3) return 'plains';
        if (val < 0.5) return 'forest';
        if (val < 0.65) return 'mountains';
        if (val < 0.75) return 'desert';
        if (val < 0.85) return 'swamp';
        if (val < 0.95) return 'tundra';
        return 'magical_grove';
    },

    /**
     * Get biome color
     */
    getBiomeColor(biome) {
        const colors = {
            water: '#2980b9',
            plains: '#27ae60',
            forest: '#1e7e34',
            mountains: '#95a5a6',
            desert: '#f39c12',
            swamp: '#16a085',
            tundra: '#ecf0f1',
            magical_grove: '#9b59b6'
        };
        return colors[biome] || '#34495e';
    },

    /**
     * Check if position has a feature
     */
    hasFeature(x, y) {
        const hash = (x * 668265263 + y * 374761393) % 100;
        return hash < 15; // 15% chance
    },

    /**
     * Get feature icon for biome
     */
    getFeatureIcon(biome, x, y) {
        const hash = (x * 374761393 + y * 668265263) % 10;
        
        const features = {
            forest: ['🌲', '🌳', '🍄'],
            plains: ['🌾', '🌻', '🌺'],
            mountains: ['⛰️', '🗻', '🏔️'],
            desert: ['🌵', '🏜️', '🐪'],
            swamp: ['🌿', '🐸', '🦎'],
            tundra: ['❄️', '⛄', '🧊'],
            magical_grove: ['✨', '🔮', '💫'],
            water: ['🌊', '🐟', '🦈']
        };
        
        const biomeFeatures = features[biome] || ['🌱'];
        return biomeFeatures[hash % biomeFeatures.length];
    },

    /**
     * Draw player
     */
    drawPlayer(ctx, gridX, gridY, cellSize) {
        const px = gridX * cellSize + cellSize / 2;
        const py = gridY * cellSize + cellSize / 2;

        // Draw player shadow
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.beginPath();
        ctx.ellipse(px, py + cellSize * 0.3, cellSize * 0.3, cellSize * 0.15, 0, 0, Math.PI * 2);
        ctx.fill();

        // Draw player character
        ctx.font = `${cellSize * 0.9}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        // Add glow effect
        ctx.shadowColor = '#667eea';
        ctx.shadowBlur = 10;
        ctx.fillStyle = '#fff';
        ctx.fillText('🧙', px, py);
        ctx.shadowBlur = 0;

        // Draw health bar above player
        const barWidth = cellSize * 0.8;
        const barHeight = 4;
        const barX = px - barWidth / 2;
        const barY = py - cellSize * 0.6;
        
        const healthPercent = Game.playerData.health / Game.playerData.max_health;
        
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(barX, barY, barWidth, barHeight);
        
        ctx.fillStyle = healthPercent > 0.5 ? '#4ade80' : healthPercent > 0.25 ? '#f39c12' : '#e74c3c';
        ctx.fillRect(barX, barY, barWidth * healthPercent, barHeight);
    },

    /**
     * Render minimap
     */
    renderMinimap() {
        if (!Game.playerData) return;

        const ctx = this.minimapCtx;
        const canvas = this.minimapCanvas;
        const size = 50; // Minimap shows 50x50 area
        const cellSize = canvas.width / size;

        // Clear
        ctx.fillStyle = '#0f0f1e';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const playerPos = Game.playerData.position;
        const centerX = Math.floor(size / 2);
        const centerY = Math.floor(size / 2);

        // Draw minimap tiles
        for (let y = 0; y < size; y++) {
            for (let x = 0; x < size; x++) {
                const worldX = Math.floor(playerPos[0]) + (x - centerX);
                const worldY = Math.floor(playerPos[1]) + (y - centerY);
                
                const biome = this.getBiomeAtPosition(worldX, worldY);
                const color = this.getBiomeColor(biome);
                
                ctx.fillStyle = color;
                ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            }
        }

        // Draw player position
        ctx.fillStyle = '#fff';
        ctx.shadowColor = '#667eea';
        ctx.shadowBlur = 5;
        ctx.beginPath();
        ctx.arc(
            centerX * cellSize + cellSize / 2,
            centerY * cellSize + cellSize / 2,
            cellSize * 0.8,
            0,
            Math.PI * 2
        );
        ctx.fill();
        ctx.shadowBlur = 0;

        // Draw border
        ctx.strokeStyle = 'rgba(102, 126, 234, 0.5)';
        ctx.lineWidth = 2;
        ctx.strokeRect(0, 0, canvas.width, canvas.height);
    }
};
