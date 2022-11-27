import sys
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from typing import List

DATASETS = "datasets/"
DATA4_TXT = "4.txt"
DATA9_TXT = "9.txt"
DATA16_TXT = "16.txt"
DATA5_TXT = "5.txt"

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
"""

def index_with_least_free_slots(puzzle,checked):
    """
    Chooses the row with least available options. 
    If several available, chooses one at random.
    """
    least = len(puzzle)*100000 # Just arbitrarily large number.
    row_with_least_free = None

    for i,row in enumerate(puzzle):
        free = check_free_spots(row)

        if (len(free) < least) and (len(free) != 0) and (i not in checked):
            least = len(free)
            row_with_least_free = i
    
    return row_with_least_free

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

def contains_invalid_numbers(lst:List[int]):
    return (max(lst) > len(lst)+1) or (min(lst) < 0)

def check_validity(puzzle):
    for i, row in enumerate(puzzle):
        if (contains_duplicates(occupied(row))):
            print(f"Row {i} contains duplicates.")
            return False
        
        if (contains_invalid_numbers(row)):
            print(f"Row {i} contains invalid numbers.")
            return False
    
    for i, col in enumerate(get_columns(puzzle)):
        if (len(col) != len(puzzle)):
            print(f"Column {i} has an invalid column length. Expected {len(puzzle)}, got {len(col)}.")

        if (contains_duplicates(occupied(col))):
            print(f"Column {i} contains duplicates")
            return False
        
        if (contains_invalid_numbers(col)):
            print(f"Column {i} contains invalid numbers")
            return False

    return True

def check_free_spots(lst):
    return [i for i, x in enumerate(lst) if x == 0]


def occupied(lst):
    return [x for x in lst if x != 0]

def contains_duplicates(lst):
    return (len(lst) - len(set(lst))) != 0 

def possibilities(lst):
    return [x+1 for x in range(len(lst))]


def check_available(lst):
    return [x for x in possibilities(lst) if x not in occupied(lst)]

def also_available_in_column(options, lst):
    # If it isn't already in the column
    return [x for x in options if x not in lst]

def get_columns(puzzle):
    cols = []
    for i in range(len(puzzle)):
        cols.append(puzzle[:,i])
    return cols

def solve(puzzle: NDArray):

    cols = get_columns(puzzle)
    asdf = 0
    while True:
        asdf+=1
        checked = []

        index = index_with_least_free_slots(puzzle,checked)
        if asdf == 10000:
            print("heheeee")
        if index == None:
            break
        
        free = check_free_spots(puzzle[index]) # Where can we insert available numbers for this row
        
        if not free:
            checked.append(index)
            continue

        available_nums = check_available(puzzle[index]) # What numbers are available for this row

        for j in free:
            insertable = also_available_in_column(available_nums, cols[j])

            if not insertable:
                checked.append(index)
                continue
            
            puzzle[index][j] = insertable[0]
            cols = get_columns(puzzle)
            checked.clear()
            break

        # print_puzzle(puzzle)
        if asdf == 100_000_000:
            break

    return puzzle
 



def main():
    parent = Path(__file__).parent.parent
    
    for x in [DATA4_TXT,DATA9_TXT,DATA16_TXT,DATA5_TXT]:
        data_path = Path.joinpath(parent, DATASETS+x)
        puzzle = collect_puzzle(data_path)
        valid = check_validity(puzzle)
        size = len(puzzle)
        puzzle_size = f"{size}x{size}"

        if not valid:
            print(f"{x} is an invalid {puzzle_size} puzzle.")
            continue

        print(f"Solving {size}x{size} puzzle...")
        solve(puzzle)
        print_puzzle(puzzle)

    


if __name__ == "__main__":
    sys.exit(main())