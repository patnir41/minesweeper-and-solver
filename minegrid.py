from minesweeper import *
import random


class MineGrid:

    def __init__(self, square, num_bombs):
        """
        Creating grid, with width and height of a square, and bombs randomly placed
        """
        self.square = square
        self.num_bombs = num_bombs
        self.bombs = self.create_bombs()
        self.val_grid = self.create_grid_val()

    def add_bombs(self, grid):
        """
        given a list of bomb coordinates, add the bomb to the correct location in grid
        x = col number
        y = row number
        after adding bombs, will update each adjacent grid cell to indicate number of adjacent bombs
        """
        for bomb_location in self.bombs:
            col = bomb_location[0]
            row = bomb_location[1]
            grid[row][col] = 'M'

            row_range = range(row - 1, row + 2)
            col_range = range(col - 1, col + 2)

            for i in row_range:
                for j in col_range:
                    if 0 <= i < len(grid) and 0 <= j < len(grid) and grid[i][j] != 'M':
                        grid[i][j] += 1

    def create_grid_val(self):
        """
        creates a 'master' grid with all cells uncovered, leaving the correct values surrounding
        mines to be checked with the playable grid
        """
        grid = [[0 for y in range(self.square)] for x in range(self.square)]
        self.add_bombs(grid)
        return grid

    def create_bombs(self):
        """
        will create bombs in random locations on the grid
        """
        total_count = self.num_bombs
        bomb_locations = []
        while total_count > 0:
            x_rand = random.randint(0, self.square - 1)
            y_rand = random.randint(0, self.square - 1)
            if [x_rand, y_rand] in bomb_locations:
                continue
            bomb_locations.append([x_rand, y_rand])
            total_count -= 1
        return bomb_locations
