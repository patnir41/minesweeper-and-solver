#!/usr/bin/env python3
"""
Minesweeper Side Project
"""

from minegrid import *
from tkinter import *
from tkinter import messagebox
from functools import partial


def mine_sweeper(square, num_bombs):
    """
    generates the game
    """
    play_grid = MineGrid(square, num_bombs)
    make_gui(play_grid)


def print_grid(grid):
    """
    will print out grid in a displayable format
    """
    for row in grid:
        print(' '.join([str(elem) for elem in row]))


def make_gui(grid_object):
    """
    creates GUI to play the game
    """
    root = Tk()
    square = grid_object.square
    buttons = []
    root.geometry('600x600')
    list_uncovered = []

    def btn_clicked(row, column):
        if grid_object.val_grid[row][column] == 'M':
            print_grid(grid_object.val_grid)
            messagebox.showinfo("Minesweeper", "YOU LOST! See mine positions in terminal.")
            exit()
        if grid_object.val_grid[row][column] == 0:
            for i in range(row - 1, row + 2):
                for j in range(column - 1, column + 2):
                    if 0 <= i < square and 0 <= j < square:
                        if [j, i] not in list_uncovered:
                            list_uncovered.append([j, i])
                        buttons[i][j].configure(text=grid_object.val_grid[i][j])
        buttons[row][column].configure(text=grid_object.val_grid[row][column])
        if [column, row] not in list_uncovered:
            list_uncovered.append([column, row])
        if len(list_uncovered) == (square ** 2) - grid_object.num_bombs:
            messagebox.showinfo("Minesweeper", "Congratulations! You WON!")
            exit()

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    field = Frame(root)
    field.grid(row=0, column=0, sticky='news')

    for row in range(grid_object.square):
        field.grid_rowconfigure(row, weight=1)
        buttons.append([])
        for column in range(grid_object.square):
            field.grid_columnconfigure(column, weight=1)
            btn = Button(field, text='■', command=partial(btn_clicked, row, column))
            buttons[row].append(btn)
            btn.grid(row=row, column=column, sticky='news')

    root.mainloop()


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        sqr = int(args[0])
        num_bombs = int(args[1])
        mine_sweeper(sqr, num_bombs)


if __name__ == '__main__':
    main()
