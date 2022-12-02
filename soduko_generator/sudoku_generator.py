import sys
from enum import Enum
from random import randint, shuffle

import numpy as np

from solver.sudoku_solver import (
    also_available_in_column,
    check_available,
    check_free_spots,
    get_columns,
    possibilities,
)

"""
TODO: Right idea, wrong execution I believe.
Instead of making a puzzle with pseudo-occupied squares,
actually occupy them, but if it is not possible to occupy a certain row with x amount of 
digits, just ignore it and jump to the next one.
"""


def check_all_nums_used(puzzle):
    poss = possibilities(puzzle[0])  # just take any random
    for row in puzzle:
        for col in row:
            if col in poss:
                poss.remove(col)

    return poss


def insert_remaining_nums(puzzle, poss_remaining):
    while poss_remaining:
        for row in puzzle:
            cols = get_columns(puzzle)
            available = check_available(row)
            free = check_free_spots(row)

            for idx in free:
                insertable = [
                    x
                    for x in poss_remaining
                    if x in also_available_in_column(available, cols[idx])
                ]

                if not insertable:
                    continue

                row[idx] = insertable[
                    randint(0, len(insertable) - 1)
                ]  # just take any random one.
                poss_remaining.remove(row[idx])

            # poss_remaining.remove(to_insert)


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


def generate_puzzle(
    size: int,
    difficulty: Difficulty,
):
    puzzle = np.zeros((size, size), int)
    diff = difficulty.value
    for ri, row in enumerate(puzzle):

        if size <= difficulty.value:
            diff = size  # Just default it to this size to avoid invalid numbers

        occupied = randint(0, size - diff)

        available_nums = check_available(row)
        indices_to_occupy = check_free_spots(row)
        shuffle(available_nums)
        shuffle(indices_to_occupy)

        indices_to_occupy = indices_to_occupy[0:occupied]

        for i in indices_to_occupy:
            cols = get_columns(puzzle)
            insertable = also_available_in_column(available_nums, cols[i])
            cnt = 0

            if not insertable:
                cnt += 1
                continue

            to_insert = insertable.pop(randint(0, len(insertable) - 1))
            if to_insert in available_nums:
                available_nums.remove(to_insert)

            puzzle[ri][i] = to_insert

    poss_remaining = check_all_nums_used(puzzle)

    if poss_remaining:
        insert_remaining_nums(puzzle, poss_remaining)

    return puzzle


def main():
    easy = generate_puzzle(5, Difficulty.EASY)
    medium = generate_puzzle(5, Difficulty.MEDIUM)
    hard = generate_puzzle(5, Difficulty.HARD)
    # print(solve(easy))
    # print(solve(medium))
    # print(solve(hard))
    print(f"easy: \n{easy}")
    print(f"medium: \n{medium}")
    print(f"hard: \n{hard}")


if __name__ == "__main__":
    sys.exit(main())
