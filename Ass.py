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
    
    return True


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

    for row in range(self.size-1, -1, -1): # For every row (in reverse order)
      for col in range(self.size): # For every column
        # Print the player in it with its symbol and a space if its not at the end
        print(self.keys[self.items[col][row]], end=('' if col == self.size - 1 else ' '))
      print('')
    print('-' * (self.size * 2 - 1)) # Divider
    for i in range(self.size): # Print the column numbers
      print(i, end=('' if i == self.size - 1 else ' '))
    print('')
    print(f'Points player 1: {self.points[0]}')
    print(f'Points player 2: {self.points[1]}')

  




class FourInARow:
  def __init__(self, size):
    self.board = GameBoard(size)

  def play(self):
    print("*****************NEW GAME*****************")
    self.board.display()
    player_number = 0
    print()
    while not self.board.game_over():
      print("Player ", player_number+1, ": ")
      if player_number == 0:
        valid_input = False
        while not valid_input:
          try:
            column = int(input("Please input slot: "))
          except ValueError:
            print(
              "Input must be an integer in the range 0 to ", self.board.size)
          else:
            if column < 0 or column >= self.board.size:
              print(
                "Input must be an integer in the range 0 to ", self.board.size)
            else:
              if self.board.add(column, player_number+1):
                valid_input = True
              else:
                print(
                  "Column ", column, "is alrady full. Please choose another one.")
      else:
        # Choose move which maximises new points for computer player
        (best_column, max_points) = self.board.column_resulting_in_max_points(2)
        if max_points > 0:
          column = best_column
        else:
          # if no move adds new points choose move which minimises points opponent player gets
          (best_column, max_points) = self.board.column_resulting_in_max_points(1)
          if max_points > 0:
            column = best_column
          else:
            # if no opponent move creates new points then choose column as close to middle as possible
            column = self.board.free_slots_as_close_to_middle_as_possible()[
              0]
        self.board.add(column, player_number+1)
        print("The AI chooses column ", column)
      self.board.display()
      player_number = (player_number+1) % 2
    if (self.board.points[0] > self.board.points[1]):
      print("Player 1 (circles) wins!")
    elif (self.board.points[0] < self.board.points[1]):
      print("Player 2 (crosses) wins!")
    else:
      print("It's a draw!")

FourInARow(6).play()