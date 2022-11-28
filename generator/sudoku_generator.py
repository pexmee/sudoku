import sys
from random import randint

import numpy as np

from solver.sudoku_solver import (
    also_available_in_column,
    check_available,
    contains_duplicates,
    get_columns,
)


class Difficulty:
    EASY = 0
    MEDIUM = 1
    HARD = 2

    def get_difficulty(level):

        if level == Difficulty.EASY:
            return Difficulty.EASY

        if level == Difficulty.MEDIUM:
            return Difficulty.MEDIUM

        if level == Difficulty.HARD:
            return Difficulty.HARD


def check_spots_to_occupy(lst):
    return [i for i, x in enumerate(lst) if x == -1]


def generate_occupied_squares(size, difficulty):
    puzzle = np.zeros((size, size), int)
    start = Difficulty.get_difficulty(difficulty)

    for row in range(size):
        occupied = randint(start, size)

        for _ in range(occupied):
            index = randint(0, size - 1)
            puzzle[row][index] = -1

    return puzzle


def done(puzzle):
    for row in puzzle:
        for num in row:
            if num == -1:
                return False

    return True


def fill_occupied_squares(puzzle):
    occupied_puzzle = np.copy(puzzle)
    cols = get_columns(occupied_puzzle)

    while not done(occupied_puzzle):
        for row in occupied_puzzle:
            available_nums = check_available(row)

            indices_to_occupy = check_spots_to_occupy(row)

            for j in indices_to_occupy:
                insertable = also_available_in_column(available_nums, cols[j])

                if not insertable:
                    continue

                row[j] = insertable.pop()  # Just take one of em
                cols = get_columns(occupied_puzzle)
                break

    return occupied_puzzle


def main():
    print(fill_occupied_squares(generate_occupied_squares(5, Difficulty.EASY)))
    print(fill_occupied_squares(generate_occupied_squares(5, Difficulty.MEDIUM)))
    print(fill_occupied_squares(generate_occupied_squares(5, Difficulty.HARD)))


if __name__ == "__main__":
    sys.exit(main())
