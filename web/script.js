// Alex McLeod - amcl287

let removeErrorTimeout;

// Get the board size, validate it, and start the game
async function startGame() {
  const sizeSelectorInput = document.querySelector('.size-selector-input');
  const selectedBoardSizeValue = sizeSelectorInput.value;
  if (sizeSelectorInput.value == '') return;
  if (selectedBoardSizeValue < 5) {
    sizeSelectorInput.value = '';
    showError('Board size cannot be less than 5');
    return;
  }
  if (selectedBoardSizeValue != Math.round(selectedBoardSizeValue)) {
    sizeSelectorInput.value = '';
    showError('Board size must be an integer value');
    return;
  }
  await eel.start_game(selectedBoardSizeValue)();
  return;
}

// Create an error snackbox in the bottom right with the error in it
function showError(err) {
  const errorSnackboxDiv = document.createElement('div');
  errorSnackboxDiv.classList.add('error-snackbox');
  errorSnackboxDiv.innerText = err;
  const body = document.querySelector('body');
  removeErrorSnackboxes();
  body.appendChild(errorSnackboxDiv);
  removeErrorTimeout = setTimeout(removeErrorSnackboxes, 3000);
}

// Hide all snackboxes
function removeErrorSnackboxes() {
  clearTimeout(removeErrorTimeout);
  document
    .querySelectorAll('.error-snackbox')
    .forEach((element) => element.remove());
}

// If the user clicks enter it starts the game
document.addEventListener('keypress', (e) => {
  if (e.key == 'Enter') startGame();
});

// For python to change webpages
eel.expose(navigate);
function navigate(url) {
  window.location.replace(url);
}
