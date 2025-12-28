/**
 * Ricochet Solver - Client-side board logic
 *
 * Board state is managed entirely on the client.
 * Walls are stored as BigInt bitmasks (225 bits for a 15x15 grid).
 */

const GRID_SIZE = 16;
const WALL_GRID_SIZE = GRID_SIZE - 1; // 15x15 for walls

// Initial wall states (center 4 squares walled off)
const VERTICAL_WALLS_START = 425365939393319416398289585530533314560n;
const HORIZONTAL_WALLS_START = 510423550856776670280647936708916019200n;

// Board state
const state = {
    selected: null, // {x, y} or null
    verticalWalls: VERTICAL_WALLS_START,
    horizontalWalls: HORIZONTAL_WALLS_START
};

// Wall coordinate helpers
function wallBitIndex(x, y) {
    return BigInt(y * WALL_GRID_SIZE + x);
}

function hasVerticalWall(x, y) {
    if (x < 0 || x >= WALL_GRID_SIZE || y < 0 || y >= WALL_GRID_SIZE) return false;
    return (state.verticalWalls & (1n << wallBitIndex(x, y))) !== 0n;
}

function hasHorizontalWall(x, y) {
    if (x < 0 || x >= WALL_GRID_SIZE || y < 0 || y >= WALL_GRID_SIZE) return false;
    return (state.horizontalWalls & (1n << wallBitIndex(x, y))) !== 0n;
}

function setVerticalWall(x, y, value) {
    if (x < 0 || x >= WALL_GRID_SIZE || y < 0 || y >= WALL_GRID_SIZE) return;
    if (isUneditableVerticalWall(x, y)) return;

    const bit = 1n << wallBitIndex(x, y);
    if (value) {
        state.verticalWalls |= bit;
    } else {
        state.verticalWalls &= ~bit;
    }
}

function setHorizontalWall(x, y, value) {
    if (x < 0 || x >= WALL_GRID_SIZE || y < 0 || y >= WALL_GRID_SIZE) return;
    if (isUneditableHorizontalWall(x, y)) return;

    const bit = 1n << wallBitIndex(x, y);
    if (value) {
        state.horizontalWalls |= bit;
    } else {
        state.horizontalWalls &= ~bit;
    }
}

function toggleVerticalWall(x, y) {
    setVerticalWall(x, y, !hasVerticalWall(x, y));
}

function toggleHorizontalWall(x, y) {
    setHorizontalWall(x, y, !hasHorizontalWall(x, y));
}

// Center area is uneditable (walls around center 4 squares)
function isUneditableVerticalWall(x, y) {
    return x >= 6 && x <= 8 && y >= 7 && y <= 8;
}

function isUneditableHorizontalWall(x, y) {
    return x >= 7 && x <= 8 && y >= 6 && y <= 8;
}

function isUnplayableCell(x, y) {
    // Center 4 cells are unplayable
    return x >= 7 && x <= 8 && y >= 7 && y <= 8;
}

// Selection
function selectCell(x, y) {
    if (state.selected && state.selected.x === x && state.selected.y === y) {
        state.selected = null; // Deselect if clicking same cell
    } else {
        state.selected = { x, y };
    }
    render();
}

// Wall toggling for selected cell
function toggleWallAbove() {
    if (!state.selected) return;
    const { x, y } = state.selected;
    if (y > 0) {
        toggleHorizontalWall(x, y - 1);
        render();
    }
}

function toggleWallBelow() {
    if (!state.selected) return;
    const { x, y } = state.selected;
    if (y < GRID_SIZE - 1) {
        toggleHorizontalWall(x, y);
        render();
    }
}

function toggleWallLeft() {
    if (!state.selected) return;
    const { x, y } = state.selected;
    if (x > 0) {
        toggleVerticalWall(x - 1, y);
        render();
    }
}

function toggleWallRight() {
    if (!state.selected) return;
    const { x, y } = state.selected;
    if (x < GRID_SIZE - 1) {
        toggleVerticalWall(x, y);
        render();
    }
}

// Check if wall can be toggled
function canToggleWallAbove() {
    if (!state.selected) return false;
    const { x, y } = state.selected;
    return y > 0 && !isUneditableHorizontalWall(x, y - 1);
}

function canToggleWallBelow() {
    if (!state.selected) return false;
    const { x, y } = state.selected;
    return y < GRID_SIZE - 1 && !isUneditableHorizontalWall(x, y);
}

function canToggleWallLeft() {
    if (!state.selected) return false;
    const { x, y } = state.selected;
    return x > 0 && !isUneditableVerticalWall(x - 1, y);
}

function canToggleWallRight() {
    if (!state.selected) return false;
    const { x, y } = state.selected;
    return x < GRID_SIZE - 1 && !isUneditableVerticalWall(x, y);
}

// Get wall state for buttons
function hasWallAbove() {
    if (!state.selected) return false;
    const { x, y } = state.selected;
    return y > 0 && hasHorizontalWall(x, y - 1);
}

function hasWallBelow() {
    if (!state.selected) return false;
    const { x, y } = state.selected;
    return y < GRID_SIZE - 1 && hasHorizontalWall(x, y);
}

function hasWallLeft() {
    if (!state.selected) return false;
    const { x, y } = state.selected;
    return x > 0 && hasVerticalWall(x - 1, y);
}

function hasWallRight() {
    if (!state.selected) return false;
    const { x, y } = state.selected;
    return x < GRID_SIZE - 1 && hasVerticalWall(x, y);
}

// Rendering
function render() {
    renderBoard();
    renderControls();
}

function renderBoard() {
    const board = document.getElementById('board');
    board.innerHTML = '';

    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';

            if (state.selected && state.selected.x === x && state.selected.y === y) {
                cell.classList.add('selected');
            }

            if (isUnplayableCell(x, y)) {
                cell.classList.add('unplayable');
            }

            // Add dot
            const dot = document.createElement('div');
            dot.className = 'dot';
            cell.appendChild(dot);

            // Add walls
            if (y > 0 && hasHorizontalWall(x, y - 1)) {
                const wall = document.createElement('div');
                wall.className = 'wall top';
                cell.appendChild(wall);
            }

            if (y < GRID_SIZE - 1 && hasHorizontalWall(x, y)) {
                const wall = document.createElement('div');
                wall.className = 'wall bottom';
                cell.appendChild(wall);
            }

            if (x > 0 && hasVerticalWall(x - 1, y)) {
                const wall = document.createElement('div');
                wall.className = 'wall left';
                cell.appendChild(wall);
            }

            if (x < GRID_SIZE - 1 && hasVerticalWall(x, y)) {
                const wall = document.createElement('div');
                wall.className = 'wall right';
                cell.appendChild(wall);
            }

            cell.addEventListener('click', () => selectCell(x, y));
            board.appendChild(cell);
        }
    }
}

function renderControls() {
    const controls = document.getElementById('controls');

    if (!state.selected) {
        controls.innerHTML = '<p class="hint">Click a cell to select it</p>';
        return;
    }

    const { x, y } = state.selected;
    controls.innerHTML = `
        <p class="selected-info">Selected: (${x}, ${y})</p>
        <div class="wall-buttons">
            <div class="button-row">
                <button
                    onclick="toggleWallAbove()"
                    ${canToggleWallAbove() ? '' : 'disabled'}
                    class="${hasWallAbove() ? 'active' : ''}"
                >
                    ${hasWallAbove() ? 'Remove' : 'Add'} Wall Above
                </button>
            </div>
            <div class="button-row middle">
                <button
                    onclick="toggleWallLeft()"
                    ${canToggleWallLeft() ? '' : 'disabled'}
                    class="${hasWallLeft() ? 'active' : ''}"
                >
                    ${hasWallLeft() ? 'Remove' : 'Add'} Left
                </button>
                <button
                    onclick="toggleWallRight()"
                    ${canToggleWallRight() ? '' : 'disabled'}
                    class="${hasWallRight() ? 'active' : ''}"
                >
                    ${hasWallRight() ? 'Remove' : 'Add'} Right
                </button>
            </div>
            <div class="button-row">
                <button
                    onclick="toggleWallBelow()"
                    ${canToggleWallBelow() ? '' : 'disabled'}
                    class="${hasWallBelow() ? 'active' : ''}"
                >
                    ${hasWallBelow() ? 'Remove' : 'Add'} Wall Below
                </button>
            </div>
        </div>
    `;
}

// Export state for server validation
function getBoardState() {
    return {
        verticalWalls: state.verticalWalls.toString(),
        horizontalWalls: state.horizontalWalls.toString()
    };
}

// Initialize
render();
