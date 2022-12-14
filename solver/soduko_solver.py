import sys
from pathlib import Path
from random import randint
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

EXIT_SUCCESS = 0
DATASETS = "datasets/"
DATA4_TXT = DATASETS + "4.txt"
DATA9_TXT = DATASETS + "9.txt"
DATA16_TXT = DATASETS + "16.txt"


class NoSolutionException(Exception):
    "Raised when puzzle has no solution"

class InvalidPuzzleException(Exception):
    "Raised when puzzle is invalid"

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


def solve(puzzle: NDArray):
    coord = get_free_spot(puzzle)
    
    if not coord:
        return True

    f_row,f_col = coord
    for num in valid_nums(puzzle):
        if insertable(puzzle, f_row,f_col, num):
            print("inserting num", num)
            puzzle[f_row][f_col] = num

            if solve(puzzle):
                return True
            
            puzzle[f_row][f_col] = 0

    return False

def insertable(puzzle: NDArray, f_row, f_col, num):
    if num not in taken_numbers(puzzle[f_row]) and num not in taken_numbers_column(puzzle,f_col):
        return True
        
    
# We could have used an index loop but this is prettier.
def valid_nums(puzzle:NDArray): 
    return [i for i in range(1,len(puzzle))]

def taken_numbers(lst):
    return [x for x in lst if x != 0]

def taken_numbers_column(puzzle: NDArray, col: int):
    return [x for x in puzzle[:,col] if x != 0]
        

def contains_duplicates(lst):
    return (len(lst) - len(set(lst))) != 0


def possibilities(lst):
    return [x + 1 for x in range(len(lst))]


def check_available(lst):
    return [x for x in possibilities(lst) if x not in taken_numbers(lst)]

def get_free_spot(puzzle: NDArray):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
                return (i,j)
    
    return None


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


def also_available_in_column(options, lst):
    # If it isn't already in the column
    return [x for x in options if x not in lst]

def get_columns(puzzle):
    cols = []
    for i in range(len(puzzle)):
        cols.append(puzzle[:, i])
    return cols

def solvable(puzzle: NDArray):
    for row in puzzle:
        cols = get_columns(puzzle)
        available = check_available(row)
        for i in check_free_spots(row):
            if also_available_in_column(available,cols[i]):
                return True
    
    return False

def sanity_check(puzzle:NDArray):
    if not check_validity(puzzle):
            raise InvalidPuzzleException("puzzle is invalid")
        
    if not solvable(puzzle):
        raise NoSolutionException("puzzle is not solvable. It has no solution.")

def done(puzzle):
    for row in puzzle:
        for col in row:
            if col == 0:
                return False

    return True

def pick_least_free(puzzle, checked):
    """
    Chooses the row with least available options.
    If several available, chooses one at random.
    """
    least = len(puzzle) * 100000  # Just arbitrarily large number.
    row_with_least_free = None

    for i, row in enumerate(puzzle):
        free = check_free_spots(row)

        if (len(free) < least) and (len(free) != 0) and (i not in checked):
            least = len(free)
            row_with_least_free = i

    return row_with_least_free


def solve_naive(puzzle: NDArray):
    puzzle = np.copy(puzzle)
    cols = get_columns(puzzle)
    checked = []

    while not done(puzzle):

        if not solvable(puzzle): # Should guarantee we don't get stuck in infinity loop
            raise NoSolutionException("puzzle has no solution")

        
        index = pick_least_free(puzzle, checked)

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

    for path in [DATA4_TXT, DATA9_TXT, DATA16_TXT]:
        data_path = Path.joinpath(parent, path)
        puzzle = collect_puzzle(data_path)
        print(f"solving {len(puzzle)}x{len(puzzle)} puzzle..")
        
        try:
            sanity_check(puzzle)

        except NoSolutionException as exc:
            print("puzzle has no solution")
            
        except InvalidPuzzleException as exc:
            print("puzzle is invalid")
        
        else: 
            naive = solve_naive(puzzle)
            if list(naive): # Just to evaluate as a bool basically
                print_puzzle(naive)

            elif solve(puzzle):
                print("successfully solved")

            else:
                print("could not find solution to puzzle")

            print_puzzle(puzzle)

if __name__ == "__main__":
    sys.exit(main())
