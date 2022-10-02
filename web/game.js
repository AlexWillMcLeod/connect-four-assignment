// Alex McLeod - amcl287

eel.expose(createBoard);
function createBoard(boardSize) {
  // Function to add the board to the page
  const grid = document.createElement('div'); // Create the grid element
  grid.classList.add('game-board-grid'); // Add a class to it for styling and js
  for (let row = 1; row <= boardSize; row++) {
    for (let col = 1; col <= boardSize; col++) {
      const newBox = document.createElement('div'); // Go through every column and row and add a box
      newBox.classList.add('game-board-grid-box');
      newBox.classList.add(`game-board-grid-box-${col}-${row}`); // Add classes to the box
      const state = document.createElement('div'); // Add a token
      state.addEventListener('click', () =>
        // If the token is clicked add a token to the column its in
        eel.add_to_column(parseInt(col) - 1)
      );
      state.style.cursor = 'pointer'; // Pointer cursor
      state.classList.add(`game-board-grid-box-state`); // Add classes
      state.classList.add(`game-board-grid-box-state-${col}-${row}`);
      state.classList.add(`state-0`); // This colours the token
      newBox.appendChild(state); // Add the token to the box
      newBox.style['grid-column'] = col;
      newBox.style['grid-row'] = boardSize - row + 1;
      grid.appendChild(newBox); // Add the box to the grid
    }
  }

  // Add grid to the grid container
  const container = document.querySelector('.game-board-grid-container');
  container.appendChild(grid);

  // Add scores into the container
  const playerOneScore = document.createElement('h1');
  playerOneScore.classList.add('game-board-grid-player-one-score');

  const playerOneScoreText = `Player Score: 0`;
  playerOneScore.innerText = playerOneScoreText;

  const computerScore = document.createElement('h1');
  computerScore.classList.add('game-board-grid-computer-score');

  const computerScoreText = `Computer Score: 0`;
  computerScore.innerText = computerScoreText;

  container.appendChild(playerOneScore);
  container.appendChild(computerScore);

  // Restart button
  const restartButton = document.createElement('button');
  restartButton.innerText = 'Restart';
  restartButton.classList.add('game-board-grid-restart-button');
  restartButton.addEventListener('click', eel.restart_game);
  container.appendChild(restartButton);
}

// Updates board so that every token is the right colour and the scores are correct
eel.expose(updateBoard);
function updateBoard(board, points) {
  for (let row = 1; row <= board.length; row++) {
    for (let col = 1; col <= board.length; col++) {
      const state = document.querySelector(
        `.game-board-grid-box-state-${col}-${row}`
      );
      console.log(`new state: ${state.classList}`);
      state.className = `game-board-grid-box-state game-board-grid-box-state-${col}-${row} state-${
        board[col - 1][row - 1]
      }`;
    }
  }
  // Update user score
  const playerOneScore = document.querySelector(
    '.game-board-grid-player-one-score'
  );

  const playerOneScoreText = `Player Score: ${points[0]}`;
  playerOneScore.innerText = playerOneScoreText;

  // Update computer score
  const computerScore = document.querySelector(
    '.game-board-grid-computer-score'
  );

  const computerScoreText = `Computer Score: ${points[1]}`;
  computerScore.innerText = computerScoreText;
}

// If the game is over, change the restart button to a replay button
eel.expose(gameOver);
function gameOver() {
  const replayButton = document.querySelector(
    '.game-board-grid-restart-button'
  );
  replayButton.innerText = 'Replay';
  replayButton.removeEventListener('click', eel.restart_game);
  replayButton.addEventListener('click', () =>
    window.location.replace('index.html')
  );
}

// Create the board in python
eel.create_board();
