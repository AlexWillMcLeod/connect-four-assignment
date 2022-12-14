# Alex McLeod - amcl287

# Extended version of the Ass.py connect 4 game with a GUI made with html, css and js (source code in the ./web folder).
# Just run this file and it will open

import eel

class GameBoard:

  def __init__(self, size):
    self.size = size
    self.num_entries = [0] * size # List for the number of items in each row
    self.items = list([[0] * size for _ in range(size)]) # Creates blank grid of items
    self.points = [0] * 2 # Sets the users points to zero initially

  keys = [' ', 'o', 'x']

  # Modified list indexing function to not go backwards when indexing
  # because that would mess up num_new_points
  def get(self, a_list, col, row):
    if col < 0: raise IndexError('No negative indices')
    if row < 0: raise IndexError('No negative indices')
    return a_list[col][row]

  def num_new_points(self, column, row, player):

    # Create a temporary items list
    # to change without affecting the actual board
    temp_items = [list(item) for item in self.items]
    temp_items[column][row] = player

    # Total number of 4 in a rows found
    total = 0

    # Vertical
    for i in range(4):
      try:
        if [self.get(temp_items, column+k-3+i, row) for k in range(4)] == [player for _ in range(4)]: 
          total += 1
      except IndexError as e: 
        pass
      except Exception as e:
        print(e)

    # Horizontal
    for i in range(4):
      try:
        if [self.get(temp_items, column, row+k-3+i) for k in range(4)] == [player for _ in range(4)]:
          total += 1
      except IndexError as e: 
        pass
      except Exception as e:
        print(e)

    # Diagonal (right to left)
    for i in range(4):
      try:
        if [self.get(temp_items, column-(k-3+i), row+k-3+i) for k in range(4)] == [player for _ in range(4)]: 
          total += 1
      except IndexError as e: 
        pass
      except Exception as e:
        print(e)

    # Diagonal (left to right)
    for i in range(4):
      try:
        if [self.get(temp_items, column+(k-3+i), row+k-3+i) for k in range(4)] == [player for _ in range(4)]:
          total += 1
      except IndexError as e: 
        pass
      except Exception as e:
        print(e)

    return total
   

  def add(self, column, player):

    # If the column does not exist
    if column >= self.size or column < 0: return False
    # If the column is full
    if self.num_free_positions_in_column(column) == 0: return False

    # Find the first row you can put it in
    row = self.num_entries[column]
    self.items[column][row] = player # Set that row to the player
    self.num_entries[column] += 1 # Increase the number of entries in that row

    self.points[player-1] += self.num_new_points(column, row, player) # Updated the number of points
    self.display() # Update the board

    if self.game_over(): # Check if the game is over
      eel.gameOver();


    return True

  def opponent_add(self):

    opp_col, opp_points = self.column_resulting_in_max_points(2) # Max points computer can make
    usr_col, usr_points = self.column_resulting_in_max_points(1) # Max points the user can make

    if usr_points > opp_points: # If blocking the user stops them getting more points than you can gain
      self.add(usr_col, 2)
    else:
      self.add(opp_col, 2) 

  # Gets the number of free positions in a column
  def num_free_positions_in_column(self, column):
    return self.items[column].count(0)

  # Returns ordered list of slots closest to the middle
  def free_slots_as_close_to_middle_as_possible(self):

    mid = (self.size-1) / 2
    free_slots = [i for i in range(self.size) if self.num_free_positions_in_column(i) > 0]
    return sorted(free_slots, key=lambda x: abs(x-mid))

  # Returns the column that would give most points and how many points in a tuple
  def column_resulting_in_max_points(self, player):
    most = ([], 0)
    for col in range(self.size):
      row = self.num_entries[col] # Find empty row
      if self.num_free_positions_in_column(col) == 0: continue # Check if the column is full
      new_points = self.num_new_points(col, row, player) # Find the points you can get in that column
      if new_points > most[1]: # If you can get more, update the most points tuple
        most = ([col], new_points)
      elif new_points == most[1]: # If you can get the same add it to the list
        most[0].append(col)
    closest_to_mid = self.free_slots_as_close_to_middle_as_possible()
    for col in closest_to_mid:
      if col in most[0]:
        return (col, most[1])

  def game_over(self):
    # Check if every column is full
    for i in range(self.size):
      if self.num_free_positions_in_column(i) > 0:
        return False
    return True

  def display(self):
    eel.updateBoard(self.items, self.points)




class FourInARow:

  # Initialise the game
  def __init__(self, size):
    self.size = size
    eel.navigate('game.html')
    self.board = GameBoard(self.size)

  # Create and display the board
  def play(self):
    eel.createBoard(self.size)
    self.board.display()      


global game

# Python function to create the game and the board
@eel.expose
def start_game(board_size):
  global game
  game = FourInARow(int(board_size))

# Python function to reset the board
@eel.expose()
def restart_game(event):
  global game
  temp_board_size = game.board.size
  game = FourInARow(int(temp_board_size))
  game.board.display()

# Python function to create the board
@eel.expose
def create_board():
  global game
  game.play()

# Python function to add a token to a column
@eel.expose
def add_to_column(col):
  global game
  if game.board.game_over(): return
  if game.board.num_free_positions_in_column(col) == 0: return
  game.board.add(col, 1)
  game.board.opponent_add()
  

eel.init('web') # Initialises Eel in the web folder
eel.start('index.html', size=(700, 700), disable_cache=True) # Opens the index page

