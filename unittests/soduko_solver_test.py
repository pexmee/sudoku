from tempfile import NamedTemporaryFile
from solver.sudoku_solver import (
    yield_rows,
    collect_puzzle,
    contains_invalid_numbers,
    check_validity,
    check_free_spots,
    taken_numbers,
    contains_duplicates,
    possibilities,
    check_available,
    also_available_in_column,
    get_columns,
    solve,
)
from random import choice
from string import ascii_letters, digits
import numpy as np
from random import randint
import pytest


def test_yield_rows():
    expected = [
        "".join(choice(ascii_letters + digits) for _ in range(5)) for _ in range(5)
    ]

    with NamedTemporaryFile() as file:
        with open(file.name, "w") as write_h:
            for row in expected:
                write_h.write(row + "\n")

        assert expected == list(yield_rows(file.name))


def test_collect_puzzle():
    expected = np.array([[randint(0, 9) for _ in range(5)] for _ in range(5)])
    writable = np.char.mod("%d", expected)

    with NamedTemporaryFile() as file:
        with open(file.name, "w") as write_h:
            for row in writable:
                write_h.write(" ".join(row) + "\n")

        puzzle = collect_puzzle(file.name)
        assert np.array_equal(expected, puzzle)


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (
            [1, 1, 2, 3],
            False,
        ),
        (
            [1, 2, 3, 4],
            False,
        ),
        (
            [5, 1],
            True,
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 51, 3],
            True,
        ),
    ],
)
def test_contains_invalid_numbers(input_data, expected):
    assert contains_invalid_numbers(input_data) == expected


def test_check_validity():
    valid = np.array(
        [
            [1, 2, 3, 4],
            [0, 3, 4, 1],
            [2, 4, 1, 0],
            [0, 0, 0, 0],
        ]
    )
    invalid1 = np.array(
        [
            [1, 2, 3, 4],
            [0, 3, 4, 4],
            [2, 4, 1, 0],
            [0, 0, 0, 0],
        ]
    )
    invalid2 = np.array(
        [
            [0, 1, 2, 3],
            [1, 3, 4, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        dtype=object,
    )
    invalid3 = np.array(
        [
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 1, 4, 1],
            [4, 3, 2, 0],
            [0, 0, 0, 0],
        ]
    )
    assert check_validity(valid) == True
    for invalid in [invalid1, invalid2, invalid3]:
        assert check_validity(invalid) == False


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (
            [1, 2, 3, 0],
            [3],
        ),
        (
            [0, 0, 0, 0],
            [0, 1, 2, 3],
        ),
        (
            [1, 2, 3, 4],
            [],
        ),
        (
            [1, 2, 3, 4, 5, 6, 0, 8, 0, 10, 0, 0],
            [6, 8, 10, 11],
        ),
    ],
)
def test_check_free_spots(input_data, expected):
    assert check_free_spots(input_data) == expected


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (
            [1, 2, 3],
            [1, 2, 3],
        ),
        (
            [1, 2, 3, 4],
            [1, 2, 3, 4],
        ),
        (
            [5, 1],
            [5, 1],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
    ],
)
def test_occupied(input_data, expected):
    assert taken_numbers(input_data) == expected


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (
            [1, 2, 3, 4],
            False,
        ),
        (
            [1, 2, 3, 5, 1, 1],
            True,
        ),
        (
            [0, 0, 0, 1, 2, 3],
            True,
        ),
        (
            [5, 4, 3, 2, 1, 0, 0, 0, 9, 10, 0, 11, 0, 0, 0, 2],
            True,
        ),
        (
            [5, 4, 3, 1, 2],
            False,
        ),
    ],
)
def test_contains_duplicates(input_data, expected):
    assert contains_duplicates(input_data) == expected


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ),
        (
            [0, 1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5, 6],
        ),
        (
            [0, 1, 2],
            [1, 2, 3],
        ),
        (
            [x for x in range(25)],
            [x + 1 for x in range(25)],
        ),
    ],
)
def test_possibilities(input_data, expected):
    assert possibilities(input_data) == expected


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (
            [1, 2, 3, 0, 5],
            [4],
        ),
        (
            [0, 0, 0, 5, 3, 2],
            [1, 4, 6],
        ),
        (
            [0 for _ in range(10)],
            [x + 1 for x in range(10)],
        ),
    ],
)
def test_check_available(input_data, expected):
    assert check_available(input_data) == expected


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (
            (
                [1, 2, 3],
                [0, 0, 3, 5, 6],
            ),
            [1, 2],
        ),
        (
            (
                [1, 2, 3, 4],
                [1,0,3,0,0,5],
            ),
            [2,4],
        ),
        (
            (
                [6,7,8],
                [1,2,3,4,5,0,0,8,9,10],
            ),
            [6,7],
        ),
        (
            (
                [5,6,7],
                [0,0,0,0,5,6,7],
            ),
            [],
        ),
    ],
)
def test_also_available_in_column(input_data, expected):
    assert also_available_in_column(*input_data) == expected

