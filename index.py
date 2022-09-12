import math


class GameBoard:

  def __init__(self, size):
    self.size = size
    self.num_entries = [0] * size
    self.items = list([[0] * size for _ in range(size)])
    self.points = [0] * 2

  keys = [' ', 'o', 'x']

  # TODO: Fix error where it does not detect new points if 
  # the disc is added to the centre of a four in a row

  def num_new_points(self, column, row, player):

    temp_items = list(self.items)
    
    _sum = 0

    # Left to Right
    k = 0
    for i in range(-3, 3):
      try:
        if temp_items[column+i][row] == player or i == 0:
          k += 1
        else:
          if k >= 4:
            _sum += k - 3
          k = 0
      except: pass

    if k >= 4: _sum += k - 3

    # Top to Bottom
    k = 0
    for i in range(-3, 3):
      try:
        if temp_items[column][row+i] == player or i == 0:
          k += 1
        else:
          if k >= 4:
            _sum += k - 3
          k = 0
      except: pass

    if k >= 4: _sum += k - 3

    # Bottom to Top - Left to Right
    k = 0
    for i in range(-3, 3):
      try:
        if temp_items[column+i][row+i] == player or i == 0:
          k += 1
        else:
          if k >= 4:
            _sum += k - 3
          k = 0
      except: pass
    
    if k >= 4: _sum += k - 3

    # Bottom to Top - Right to Left
    k = 0
    for i in range(-3, 3):
      try:
        if temp_items[column-i][row+i] == player or i == 0:
          k += 1
        else:
          if k >= 4:
            _sum += k - 3
          k = 0
      except: pass

    if k >= 4: _sum += k - 3

    return _sum   
   

  def add(self, column, player):

    if column >= self.size or column < 0: return False
    if self.num_free_positions_in_column(column) == 0: return False

    row = self.num_entries[column]
    self.items[column][row] = player
    self.num_entries[column] += 1

    self.points[player-1] += self.num_new_points(column, row, player)

    return True


  def num_free_positions_in_column(self, column):
    return self.items[column].count(0)


  def free_slots_as_close_to_middle_as_possible(self):

    mid = (self.size-1) / 2
    free_slots = [i for i in range(self.size) if self.num_free_positions_in_column(i) > 0]
    return sorted(free_slots, key=lambda x: abs(x-mid))

  def column_resulting_in_max_points(self, player):
    most_points = 0
    col_most_points = []
    for column in range(self.size):
      if self.num_free_positions_in_column(column) == 0: continue
      row = self.num_entries[column]
      new_points = self.num_new_points(column, row, player)
      if new_points > most_points: col_most_points = [column]
      if new_points == most_points: col_most_points.append(column)
    for num in self.free_slots_as_close_to_middle_as_possible():
      if num in col_most_points: return (num, most_points)


  def game_over(self):
    for i in range(self.size):
      if self.num_free_positions_in_column(i) > 0:
        return False
    return True

  def display(self):

    for row in range(self.size-1, -1, -1):
      for col in range(self.size):
        print(self.keys[self.items[col][row]], end=('' if col == self.size - 1 else ' '))
      print('')
    print('-' * (self.size * 2 - 1))
    for i in range(self.size):
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

FourInARow(10).play()