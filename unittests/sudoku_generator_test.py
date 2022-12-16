from soduko_generator.sudoku_generator import generate_puzzle, Difficulty, check_all_nums_used,insert_remaining_nums
import pytest
import numpy as np

@pytest.mark.repeat(50)
@pytest.mark.parametrize(
    "size,difficulty_input",
    [
        (
            5,
            Difficulty.EASY,
        ),
        (
            10,
            Difficulty.MEDIUM,
        ),
        (
            25,
            Difficulty.HARD,
        )
    ],
)
def test_generate_puzzle(size, difficulty_input):
    puzzle = generate_puzzle(size, difficulty_input)
    for row in puzzle:
        cnt = 0
        for col in row:
            if int(col) != 0:
                cnt+=1
            
        assert len(check_all_nums_used(puzzle)) == 0


def test_check_all_nums_used():
    approved = np.array([[1,0,2],
                        [0,0,0],
                        [0,1,3]])

    discarded = np.array([[1,2,0],
                        [0,0,0],
                        [0,0,1]])
    assert len(check_all_nums_used(approved)) == 0
    assert len(check_all_nums_used(discarded)) > 0

@pytest.mark.repeat(500)
def test_insert_remaining_nums():
    small_puzzle = np.array([[0,0,0],
                        [0,0,0],
                        [0,0,0]])
    large_puzzle = np.array([[1,2,3,0,0,0,0,0],
    [1,2,3,0,0,0,0,0],
    [3,1,2,0,0,0,0,0],
    [2,3,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],])

    assert len(check_all_nums_used(insert_remaining_nums(small_puzzle,check_all_nums_used(small_puzzle)))) == 0
    assert len(check_all_nums_used(insert_remaining_nums(large_puzzle,check_all_nums_used(large_puzzle)))) == 0
