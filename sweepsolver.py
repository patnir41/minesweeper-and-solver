from minesweeper import *
from minegrid import *
import time

"""
MINESWEEPER SOLVER
"""

"""
Algorithm:
--------------------
main variables:
list of uncovered_mines
list of known_mines
dictionary of potential mines for each 'tally' count (equivalent to a proportionate risk amount 
based on uncovered cell values)
    -tuple of cell coordinates as key and 'tally' count as value

1. Uncover the first cell (top left) by default
2. Create "tally" count for each adjacent covered block

AFTER CELL IS UNCOVERED:
    *look at all surrounding uncovered cells
        -uncover the cell with the lowest tally count
        -if 'n' uncovered blocks are adjacent to a block with value 'n', those are all mines
        -if any uncovered cell is 0, all adjacent cells immediately should be uncovered

Goal - continue uncovering cells until total amount of cells that are not a mine are cleared
"""
SQUARE = 10
TOTAL_MINES = 10


def print_grid(grid):
    for row in grid:
        print(' '.join([str(elem) for elem in row]))


def solve_board():
    master = MineGrid(SQUARE, TOTAL_MINES)
    test = TestGrid(master.val_grid)
    cell = (0, 0)
    test.uncover_cell(cell)
    while not test.end_game:
        lowest_pair = min(test.tally_count.items(), key=lambda pair: pair[1])
        cell = lowest_pair[0]
        test.uncover_cell(cell)

    if test.won_game:
        #print_grid(test.test_grid)
        return 1

    return 0


class TestGrid:

    def __init__(self, key_grid):
        """
        Creating test grid of squares, with width and height of a square
        """
        self.key_grid = key_grid
        self.test_grid = [['■' for col in range(SQUARE)] for row in range(SQUARE)]
        self.mines_found = []
        self.cells_uncovered = []
        self.tally_count = {}
        self.end_game = False
        self.won_game = False

    def is_adjacent(self, mine, cell):
        """
        returns True or False if a cell is adjacent to another (noted as 'mine' for the purpose of its use in
        my code)
        """
        mine_row = mine[1]
        mine_col = mine[0]
        cell_row = cell[1]
        cell_col = cell[0]
        if mine_col in range(cell_col - 1, cell_col + 2) and mine_row in range(cell_row - 1, cell_row + 2):
            return True
        return False

    def adj_mines(self, cell):
        """
        will return the number of adjacent mines to a cell
        """
        count = 0
        for mine in self.mines_found:
            if self.is_adjacent(mine, cell):
                count += 1
        return count

    def get_surrounding_covereds(self, cell):
        """
        will return list of adjacent cells that are covered around a cell
        """
        row = cell[1]
        col = cell[0]
        surround_list = []
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (c, r) not in self.cells_uncovered:
                    surround_list.append((c, r))
        return surround_list

    def analyze_cell(self, cell):
        """
        given uncovered cell, will determine if there are adjacent mines
         -will also uncover all surrounding cells if number of adjacent mines is equal to the value in the
          uncovered block
        """
        row = cell[1]
        col = cell[0]
        cell_val = self.test_grid[row][col]
        surround_covered_cells = self.get_surrounding_covereds(cell)
        if cell_val == len(surround_covered_cells):
            for cell in surround_covered_cells:
                if cell not in self.mines_found:
                    self.mines_found.append(cell)
                    if cell in self.tally_count:
                        del self.tally_count[cell]
        if cell_val == self.get_surround_mines(cell):
            self.uncover_surrounding(cell)

    def count_tally(self):
        """
        will determine the 'tally' count for each covered cell in the grid adjacent to an uncovered cell by looping
        through each uncovered cell
        """
        for cell in self.cells_uncovered:
            row = cell[1]
            col = cell[0]
            if self.get_surrounding_covereds(cell) == 0 or self.test_grid[row][col] == 0:
                continue
            self.analyze_cell(cell)
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if (0 <= r < SQUARE and 0 <= c < SQUARE) and (c, r) not in self.cells_uncovered \
                            and (c, r) not in self.mines_found:
                        if (c, r) not in self.tally_count:
                            self.tally_count[(c, r)] = 0
                        self.tally_count[(c, r)] += (self.key_grid[row][col] - self.adj_mines(cell))

    def uncover_surrounding(self, cell):
        """
        calls uncover_cell to all surrounding covered cells
        """
        row = cell[1]
        col = cell[0]
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (0 <= r < SQUARE and 0 <= c < SQUARE) and (c, r) not in self.cells_uncovered:
                    if (c, r) not in self.mines_found:
                        self.uncover_cell((c, r))

    def uncover_cell(self, cell):
        """
         WHEN UNCOVERING A CELL:
            - if cell value is M, player has lost
            - if cell is the last one to be uncovered, player has won
            - if cell is 0, uncover all surrounding cells
            - else, reveal number in the block and add to uncovered cells
        """
        row = cell[1]
        col = cell[0]
        key_val = self.key_grid[row][col]
        if key_val == 'M':
            self.end_game = True
            return
        self.test_grid[row][col] = key_val
        self.cells_uncovered.append(cell)
        if cell in self.tally_count:
            del self.tally_count[cell]
        if len(self.cells_uncovered) == SQUARE**2 - TOTAL_MINES:
            self.won_game = True
            self.end_game = True
            return
        if key_val == 0:
            self.uncover_surrounding(cell)
        self.count_tally()

    def get_surround_mines(self, cell):
        """
        will return the number of mines that are surrounding a cell
        """
        row = cell[1]
        col = cell[0]
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (c, r) in self.mines_found:
                    count += 1
        return count


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        runs = int(args[0])
        count = 0
        for i in range(runs):
            count += solve_board()
        print(count, "successful runs out of", runs, "attempts")


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Completion time: %s minutes" % '%.2f'%((time.time() - start_time)/60))
