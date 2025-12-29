/**
 * See game_board.py for explaination of the state
 */

const GRID_SIZE = 16;

// Initial wall states (center 4 squares walled off)
const VERTICAL_WALLS_START_STATE = 108892018949695039453121004136991178096640n;
const HORIZONTAL_WALLS_START_STATE =
  130668428928063984375413354889719870128128n;

// Colors matching game_board.py
const COLORS = ["red", "blue", "green", "yellow"];

const state = {
  selected: null,
  verticalWalls: VERTICAL_WALLS_START_STATE,
  horizontalWalls: HORIZONTAL_WALLS_START_STATE,
  pieces: {
    red: null,
    blue: null,
    green: null,
    yellow: null,
  },
  target: null,
};

// Wall coordinate helpers
function wallBitIndex(x, y) {
  return BigInt(y * GRID_SIZE + x);
}

function hasVerticalWall(x, y) {
  if (x < 0 || x >= GRID_SIZE - 1 || y < 0 || y >= GRID_SIZE) return false;

  return (state.verticalWalls & (1n << wallBitIndex(x, y))) !== 0n;
}

function hasHorizontalWall(x, y) {
  if (x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE - 1) return false;
  return (state.horizontalWalls & (1n << wallBitIndex(x, y))) !== 0n;
}

function setVerticalWall(x, y, value) {
  if (x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE) return;
  if (isUneditableVerticalWall(x, y)) return;

  const bit = 1n << wallBitIndex(x, y);
  if (value) {
    state.verticalWalls |= bit;
  } else {
    state.verticalWalls &= ~bit;
  }
}

function setHorizontalWall(x, y, value) {
  if (x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE) return;
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

// Piece helpers
function getPieceAt(x, y) {
  for (const color of COLORS) {
    const piece = state.pieces[color];
    if (piece && piece.x === x && piece.y === y) {
      return color;
    }
  }
  return null;
}

function setPiece(color, x, y) {
  if (isUnplayableCell(x, y)) return;
  // Check if another piece is already there
  const existingPiece = getPieceAt(x, y);
  if (existingPiece && existingPiece !== color) return;

  state.pieces[color] = { x, y };
  render();
}

function removePiece(color) {
  state.pieces[color] = null;
  render();
}

function togglePiece(color) {
  if (!state.selected) return;
  const { x, y } = state.selected;

  const currentPiece = state.pieces[color];
  if (currentPiece && currentPiece.x === x && currentPiece.y === y) {
    // Remove piece if it's already here
    removePiece(color);
  } else {
    // Place piece here (will fail if another piece is there)
    setPiece(color, x, y);
  }
}

// Target helpers
function getTargetAt(x, y) {
  if (state.target && state.target.x === x && state.target.y === y) {
    return state.target.color;
  }
  return null;
}

function setTarget(color, x, y) {
  if (isUnplayableCell(x, y)) return;
  state.target = { x, y, color };
  render();
}

function removeTarget() {
  state.target = null;
  render();
}

function toggleTarget(color) {
  if (!state.selected) return;
  const { x, y } = state.selected;

  if (
    state.target &&
    state.target.x === x &&
    state.target.y === y &&
    state.target.color === color
  ) {
    // Remove target if same color is already here
    removeTarget();
  } else {
    // Set target here with this color
    setTarget(color, x, y);
  }
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
  const board = document.getElementById("board");
  board.innerHTML = "";

  for (let y = 0; y < GRID_SIZE; y++) {
    for (let x = 0; x < GRID_SIZE; x++) {
      const cell = document.createElement("div");
      cell.className = "cell";

      if (state.selected && state.selected.x === x && state.selected.y === y) {
        cell.classList.add("selected");
      }

      if (isUnplayableCell(x, y)) {
        cell.classList.add("unplayable");
      }

      // Add target (rendered behind piece)
      const targetColor = getTargetAt(x, y);
      if (targetColor) {
        const target = document.createElement("div");
        target.className = `target target-${targetColor}`;
        cell.appendChild(target);
      }

      // Add piece or dot
      const pieceColor = getPieceAt(x, y);
      if (pieceColor) {
        const piece = document.createElement("div");
        piece.className = `piece piece-${pieceColor}`;
        cell.appendChild(piece);
      } else {
        const dot = document.createElement("div");
        dot.className = "dot";
        cell.appendChild(dot);
      }

      // Add walls
      if (y > 0 && hasHorizontalWall(x, y - 1)) {
        const wall = document.createElement("div");
        wall.className = "wall top";
        cell.appendChild(wall);
      }

      if (y < GRID_SIZE - 1 && hasHorizontalWall(x, y)) {
        const wall = document.createElement("div");
        wall.className = "wall bottom";
        cell.appendChild(wall);
      }

      if (x > 0 && hasVerticalWall(x - 1, y)) {
        const wall = document.createElement("div");
        wall.className = "wall left";
        cell.appendChild(wall);
      }

      if (x < GRID_SIZE - 1 && hasVerticalWall(x, y)) {
        const wall = document.createElement("div");
        wall.className = "wall right";
        cell.appendChild(wall);
      }

      cell.addEventListener("click", () => selectCell(x, y));
      board.appendChild(cell);
    }
  }
}

function renderStateInfo() {
  const encoded = getEncodedState();
  return `
    <div class="state-info">
      <div class="state-row"><span class="state-label">vertical_walls:</span> <span class="state-value">${encoded.vertical_walls}</span></div>
      <div class="state-row"><span class="state-label">horizontal_walls:</span> <span class="state-value">${encoded.horizontal_walls}</span></div>
      <div class="state-row"><span class="state-label">pieces:</span> <span class="state-value">${encoded.pieces}</span></div>
      <div class="state-row"><span class="state-label">target:</span> <span class="state-value">${encoded.target !== null ? encoded.target : "None"}</span></div>
      <div class="state-row"><span class="state-label">target_color:</span> <span class="state-value">${encoded.target_color !== null ? encoded.target_color : "None"}</span></div>
    </div>
  `;
}

function renderControls() {
  const controls = document.getElementById("controls");

  const resetButton =
    '<div class="reset-section"><button onclick="resetBoard()">Reset Board</button></div>';
  const stateInfo = renderStateInfo();

  if (!state.selected) {
    controls.innerHTML =
      '<p class="hint">Click a cell to select it</p>' + resetButton + stateInfo;
    return;
  }

  const { x, y } = state.selected;
  const isUnplayable = isUnplayableCell(x, y);
  const pieceHere = getPieceAt(x, y);
  const targetHere = getTargetAt(x, y);

  // Generate piece buttons
  const pieceButtons = COLORS.map((color) => {
    const hasPiece = state.pieces[color];
    const isHere = hasPiece && hasPiece.x === x && hasPiece.y === y;
    const canPlace = !isUnplayable && (!pieceHere || pieceHere === color);
    return `
            <button
                onclick="togglePiece('${color}')"
                ${canPlace ? "" : "disabled"}
                class="piece-btn piece-btn-${color} ${isHere ? "active" : ""}"
            >
                ${isHere ? "Remove" : "Place"} ${
      color.charAt(0).toUpperCase() + color.slice(1)
    }
            </button>
        `;
  }).join("");

  // Generate target buttons
  const targetButtons = COLORS.map((color) => {
    const isHere = targetHere === color;
    const canPlace = !isUnplayable;
    return `
            <button
                onclick="toggleTarget('${color}')"
                ${canPlace ? "" : "disabled"}
                class="target-btn target-btn-${color} ${isHere ? "active" : ""}"
            >
                ${isHere ? "Remove" : "Set"} ${
      color.charAt(0).toUpperCase() + color.slice(1)
    } Target
            </button>
        `;
  }).join("");

  controls.innerHTML = `
        <p class="selected-info">Selected: (${x}, ${y})</p>

        <div class="control-section">
            <h3>Pieces</h3>
            <div class="button-grid">
                ${pieceButtons}
            </div>
        </div>

        <div class="control-section">
            <h3>Target</h3>
            <div class="button-grid">
                ${targetButtons}
            </div>
        </div>

        <div class="control-section">
            <h3>Walls</h3>
            <div class="wall-buttons">
                <div class="button-row">
                    <button
                        onclick="toggleWallAbove()"
                        ${canToggleWallAbove() ? "" : "disabled"}
                        class="${hasWallAbove() ? "active" : ""}"
                    >
                        ${hasWallAbove() ? "Remove" : "Add"} Wall Above
                    </button>
                </div>
                <div class="button-row middle">
                    <button
                        onclick="toggleWallLeft()"
                        ${canToggleWallLeft() ? "" : "disabled"}
                        class="${hasWallLeft() ? "active" : ""}"
                    >
                        ${hasWallLeft() ? "Remove" : "Add"} Left
                    </button>
                    <button
                        onclick="toggleWallRight()"
                        ${canToggleWallRight() ? "" : "disabled"}
                        class="${hasWallRight() ? "active" : ""}"
                    >
                        ${hasWallRight() ? "Remove" : "Add"} Right
                    </button>
                </div>
                <div class="button-row">
                    <button
                        onclick="toggleWallBelow()"
                        ${canToggleWallBelow() ? "" : "disabled"}
                        class="${hasWallBelow() ? "active" : ""}"
                    >
                        ${hasWallBelow() ? "Remove" : "Add"} Wall Below
                    </button>
                </div>
            </div>
        </div>

        ${resetButton}
        ${stateInfo}
    `;
}

// Export state for server validation
function getBoardState() {
  return {
    verticalWalls: state.verticalWalls.toString(),
    horizontalWalls: state.horizontalWalls.toString(),
    pieces: { ...state.pieces },
    target: state.target ? { ...state.target } : null,
  };
}

// Encode state in game_board.py format
function encodePosition(x, y) {
  // 8-bit encoding: y * 16 + x
  return y * GRID_SIZE + x;
}

function encodePieces() {
  // 32-bit integer: red (bits 0-7), blue (bits 8-15), green (bits 16-23), yellow (bits 24-31)
  let result = 0;
  const colorOrder = ["red", "blue", "green", "yellow"];
  for (let i = 0; i < colorOrder.length; i++) {
    const piece = state.pieces[colorOrder[i]];
    if (piece) {
      const pos = encodePosition(piece.x, piece.y);
      result |= pos << (i * 8);
    }
  }
  return result;
}

function encodeTarget() {
  if (!state.target) return null;
  return encodePosition(state.target.x, state.target.y);
}

function encodeTargetColor() {
  if (!state.target) return null;
  const colorIndex = COLORS.indexOf(state.target.color);
  return colorIndex >= 0 ? colorIndex : null;
}

function getEncodedState() {
  return {
    vertical_walls: state.verticalWalls.toString(),
    horizontal_walls: state.horizontalWalls.toString(),
    pieces: encodePieces(),
    target: encodeTarget(),
    target_color: encodeTargetColor(),
  };
}

// Set board state from external data
function setBoardState(data) {
  // Handle legacy call with two arguments (verticalWalls, horizontalWalls)
  if (arguments.length === 2) {
    const [verticalWalls, horizontalWalls] = arguments;
    state.verticalWalls = BigInt(verticalWalls);
    state.horizontalWalls = BigInt(horizontalWalls);
  } else {
    // New format with full state object
    if (data.verticalWalls !== undefined) {
      state.verticalWalls = BigInt(data.verticalWalls);
    }
    if (data.horizontalWalls !== undefined) {
      state.horizontalWalls = BigInt(data.horizontalWalls);
    }
    if (data.pieces !== undefined) {
      state.pieces = { ...data.pieces };
    }
    if (data.target !== undefined) {
      state.target = data.target ? { ...data.target } : null;
    }
  }

  // Ensure center walls are always set
  state.verticalWalls |= VERTICAL_WALLS_START_STATE;
  state.horizontalWalls |= HORIZONTAL_WALLS_START_STATE;

  render();
}

// Reset board to initial state
function resetBoard() {
  state.verticalWalls = VERTICAL_WALLS_START_STATE;
  state.horizontalWalls = HORIZONTAL_WALLS_START_STATE;
  state.pieces = { red: null, blue: null, green: null, yellow: null };
  state.target = null;
  state.selected = null;
  render();
}

// Load state from server
async function loadStateFromServer() {
  try {
    const response = await fetch("/api/initial-state");
    const data = await response.json();
    setBoardState(data.verticalWalls, data.horizontalWalls);
  } catch (error) {
    console.error("Failed to load state from server:", error);
  }
}

// Initialize
render();
