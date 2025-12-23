/**
 * Fractal Worlds RPG - UI Helper
 * Handles UI updates, messages, and overlays
 */

const UI = {
    messageTimeout: null,

    /**
     * Update player UI elements
     */
    updatePlayerUI(playerData) {
        // Player name and level
        document.getElementById('playerNameDisplay').textContent = playerData.name;
        document.getElementById('playerLevel').textContent = playerData.level;
        document.getElementById('playerXP').textContent = playerData.experience;

        // Health bar
        const healthPercent = (playerData.health / playerData.max_health) * 100;
        document.getElementById('healthBar').style.width = healthPercent + '%';
        document.getElementById('healthText').textContent = 
            `${Math.round(playerData.health)}/${Math.round(playerData.max_health)}`;

        // Mana bar
        const manaPercent = (playerData.mana / playerData.max_mana) * 100;
        document.getElementById('manaBar').style.width = manaPercent + '%';
        document.getElementById('manaText').textContent = 
            `${Math.round(playerData.mana)}/${Math.round(playerData.max_mana)}`;

        // Stamina bar (if available)
        if (playerData.stamina !== undefined) {
            const staminaPercent = (playerData.stamina / playerData.max_stamina) * 100;
            document.getElementById('staminaBar').style.width = staminaPercent + '%';
            document.getElementById('staminaText').textContent = 
                `${Math.round(playerData.stamina)}/${Math.round(playerData.max_stamina)}`;
        }

        // Stats
        if (playerData.stats) {
            document.getElementById('statStrength').textContent = 
                Math.round(playerData.stats.strength || 10);
            document.getElementById('statIntelligence').textContent = 
                Math.round(playerData.stats.intelligence || 10);
            document.getElementById('statAgility').textContent = 
                Math.round(playerData.stats.agility || 10);
            document.getElementById('statLogic').textContent = 
                (playerData.stats.logic_mastery || 1.0).toFixed(1);
        }

        // Position
        document.getElementById('playerPosition').textContent = 
            `${Math.round(playerData.position[0])}, ${Math.round(playerData.position[1])}, ${Math.round(playerData.position[2])}`;

        // Biome (if available)
        if (playerData.biome) {
            document.getElementById('currentBiome').textContent = 
                this.formatBiomeName(playerData.biome);
        }

        // Inventory
        this.updateInventory(playerData.inventory_count || 0, playerData.inventory || []);
    },

    /**
     * Update inventory display
     */
    updateInventory(count, items) {
        document.getElementById('inventoryCount').textContent = count;
        
        const inventoryGrid = document.getElementById('inventoryGrid');
        inventoryGrid.innerHTML = '';

        if (!items || items.length === 0) {
            inventoryGrid.innerHTML = '<div class="empty-inventory">No items yet</div>';
            return;
        }

        items.forEach((item, index) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'inventory-item';
            itemDiv.title = `${item.name} (${item.type})`;
            
            // Get item icon
            const icon = this.getItemIcon(item);
            itemDiv.innerHTML = `
                ${icon}
                ${item.quantity > 1 ? `<span class="item-quantity">${item.quantity}</span>` : ''}
            `;
            
            // Add click handler
            itemDiv.addEventListener('click', () => {
                this.showItemDetails(item);
            });
            
            inventoryGrid.appendChild(itemDiv);
        });
    },

    /**
     * Get item icon based on type
     */
    getItemIcon(item) {
        const icons = {
            weapon: '⚔️',
            armor: '🛡️',
            resource: '🔮',
            spell_rune: '📜',
            potion: '🧪',
            food: '🍖'
        };
        return icons[item.type] || '📦';
    },

    /**
     * Show item details (could be enhanced with a modal in the future)
     */
    showItemDetails(item) {
        // TODO: Replace alert with custom modal for better UX
        const details = `
            Item: ${item.name}
            Type: ${item.type}
            ${item.power ? 'Power: ' + item.power : ''}
            ${item.quantity > 1 ? 'Quantity: ' + item.quantity : ''}
        `;
        // Temporary: using console.log instead of alert for better UX
        console.log('Item Details:', item);
        this.showMessage(`${item.name} - ${item.type}${item.quantity > 1 ? ' (' + item.quantity + ')' : ''}`, 'info');
    },

    /**
     * Format biome name for display
     */
    formatBiomeName(biome) {
        return biome
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    },

    /**
     * Show a game message
     */
    showMessage(text, type = 'info') {
        const container = document.getElementById('gameMessages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `game-message ${type}`;
        messageDiv.textContent = text;
        
        container.appendChild(messageDiv);

        // Remove after 3 seconds
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            messageDiv.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.parentNode.removeChild(messageDiv);
                }
            }, 300);
        }, 3000);

        // Limit to 3 messages
        while (container.children.length > 3) {
            container.removeChild(container.firstChild);
        }
    },

    /**
     * Show combat overlay
     */
    showCombat(encounter) {
        const overlay = document.getElementById('combatOverlay');
        const info = document.getElementById('combatInfo');
        
        info.innerHTML = `
            <h3>Enemy: ${encounter.enemy_name || 'Unknown Creature'}</h3>
            <p>Level: ${encounter.enemy_level || '?'}</p>
            <p>${encounter.description || 'A hostile creature blocks your path!'}</p>
        `;
        
        overlay.classList.remove('hidden');
    },

    /**
     * Hide combat overlay
     */
    hideCombat() {
        document.getElementById('combatOverlay').classList.add('hidden');
    },

    /**
     * Show menu
     */
    showMenu() {
        document.getElementById('menuOverlay').classList.remove('hidden');
    },

    /**
     * Hide menu
     */
    hideMenu() {
        document.getElementById('menuOverlay').classList.add('hidden');
    },

    /**
     * Toggle menu
     */
    toggleMenu() {
        const menu = document.getElementById('menuOverlay');
        if (menu.classList.contains('hidden')) {
            this.showMenu();
        } else {
            this.hideMenu();
        }
    }
};
