import sys
from pathlib import Path
from random import randint
from typing import List

import numpy as np
from numpy.typing import NDArray

DATASETS = "datasets/"
DATA4_TXT = DATASETS + "4.txt"
DATA9_TXT = DATASETS + "9.txt"
DATA16_TXT = DATASETS + "16.txt"


"""
~ Sudoku solver ~

We need to know what indices are free, and what numbers are occupied currently on the current row and 
the columns below it. The best way is to iterate through the whole board, check all possible ways to
enter a digit in a free spot, and then recalculate everything. That way we should be able to find a solution.
Possibly build a parallel puzzle for this.

for each row and column we:
    * check what positions are available in the row
    * what numbers are already taken

Might have to do something like this every time:
    * go through all rows and choose the one with the least options
    * choose the corresponding column of available columns with the least option 

TODO: Make sure that the solver can try all possible permutations of the puzzle if it couldn't solve it the first way.
    * And once it has tried all possible permutations, make it say it is unsolvable. 
    - This could be impossible if the puzzle is mega large but meh let's just multithread this shit.
    - Multithread the solver by letting threads handle different parts of the puzzle. 
"""

class NoSolutionException(Exception):
    "Raised when puzzle has no solution"

class InvalidPuzzleException(Exception):
    "Raised when puzzle is invalid"

def pick_random_index(puzzle, checked):
    """
    Chooses the row with least available options.
    If several available, chooses one at random.
    """
   
    if len(checked) == len(puzzle):
        raise NoSolutionException("not solvable")
    
    occupied = 0
    row_index = randint(0,len(puzzle)-1)
    while row_index in checked:
        row_index = randint(0,len(puzzle)-1)

        if row_index not in check_free_spots(puzzle[row_index]):
            occupied += 1

        if occupied >= len(puzzle) - len(checked):
            raise NoSolutionException("wtf")
    
    return row_index



def print_puzzle(puzzle):
    print("Puzzle:")

    for row in puzzle:
        print(row)


def yield_rows(data_path: Path):
    with open(data_path) as read_h:
        for row in read_h:
            row = row.strip()
            if row:
                yield row


def collect_puzzle(data_path: Path):
    puzzle = []

    for row in yield_rows(data_path):
        puzzle.append([int(x) for x in row.split()])

    puzzle = np.array(puzzle)
    return puzzle


def contains_invalid_numbers(lst):
    return (max(lst) > len(lst) + 1) or (min(lst) < 0)


def check_validity(puzzle):
    for i, row in enumerate(puzzle):
        if contains_duplicates(taken_numbers(row)):
            print(f"Row {i} contains duplicates.")
            return False

        if contains_invalid_numbers(row):
            print(f"Row {i} contains invalid numbers.")
            return False

    for i, col in enumerate(get_columns(puzzle)):
        if len(col) != len(puzzle):
            print(
                f"Column {i} has an invalid column length. Expected {len(puzzle)}, got {len(col)}."
            )

        if contains_duplicates(taken_numbers(col)):
            print(f"Column {i} contains duplicates")
            return False

        if contains_invalid_numbers(col):
            print(f"Column {i} contains invalid numbers")
            return False

    return True


def check_free_spots(lst):
    return [i for i, x in enumerate(lst) if x == 0]


def taken_numbers(lst):
    return [x for x in lst if x != 0]


def contains_duplicates(lst):
    return (len(lst) - len(set(lst))) != 0


def possibilities(lst):
    return [x + 1 for x in range(len(lst))]


def check_available(lst):
    return [x for x in possibilities(lst) if x not in taken_numbers(lst)]


def also_available_in_column(options, lst):
    # If it isn't already in the column
    return [x for x in options if x not in lst]


def get_columns(puzzle):
    cols = []
    for i in range(len(puzzle)):
        cols.append(puzzle[:, i])
    return cols


def done(puzzle):
    for row in puzzle:
        for col in row:
            if col == 0:
                return False

    return True

def solvable(puzzle: NDArray):
    for row in puzzle:
        cols = get_columns(puzzle)
        available = check_available(row)
        for i in check_free_spots(row):
            if also_available_in_column(available,cols[i]):
                return True
    
    return False




def solve(puzzle: NDArray):
    valid = check_validity(puzzle)
    size = len(puzzle)
    puzzle_size = f"{size}x{size}"
    
    if not valid:
        raise InvalidPuzzleException(f"invalid {puzzle_size} puzzle.")

    if not solvable(puzzle):
        raise NoSolutionException(f"{puzzle_size} puzzle has no solution")


    puzzle = np.copy(puzzle)
    print(f"Solving {size}x{size} puzzle...")
    cols = get_columns(puzzle)
    checked = []

    while not done(puzzle):

        if not solvable(puzzle):
            raise NoSolutionException("puzzle has no solution")

        
        index = pick_random_index(puzzle, checked)

        if index == None:
            raise IndexError("PANIC, this should never happen")


        free = check_free_spots(
            puzzle[index]
        )  # Where can we insert available numbers for this row

        if not free:
            checked.append(index)
            continue

        available_nums = check_available(
            puzzle[index]
        )  # What numbers are available for this row

        for j in free:
            insertable = also_available_in_column(available_nums, cols[j])

            if not insertable:
                # checked.append(index) I think we should not add checked here.
                continue

            puzzle[index][j] = insertable[randint(0, len(insertable) - 1)]
            cols = get_columns(puzzle)
            checked.clear()
            break

    return puzzle


def main():
    """
    This is mostly here to lab around.
    Use soduko_solver_test to test everything.
    """
    parent = Path(__file__).parent.parent

    for i in range(100):
        for path in [DATA4_TXT]:
            data_path = Path.joinpath(parent, path)
            puzzle = collect_puzzle(data_path)
            try:
                puzzle = solve(puzzle)
            except Exception:
                pass
            else:
                print("SUCCESS")
            print(puzzle)
            print_puzzle(puzzle)


if __name__ == "__main__":
    sys.exit(main())
