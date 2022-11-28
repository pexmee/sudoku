from pathlib import Path
from random import choice, randint
from string import ascii_letters, digits
from tempfile import NamedTemporaryFile

import numpy as np
import pytest

from solver.sudoku_solver import (
    DATA4_TXT,
    DATA9_TXT,
    DATA16_TXT,
    also_available_in_column,
    check_available,
    check_free_spots,
    check_validity,
    collect_puzzle,
    contains_duplicates,
    contains_invalid_numbers,
    get_columns,
    possibilities,
    print_puzzle,
    solve,
    taken_numbers,
    yield_rows,
)


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
                [1, 0, 3, 0, 0, 5],
            ),
            [2, 4],
        ),
        (
            (
                [6, 7, 8],
                [1, 2, 3, 4, 5, 0, 0, 8, 9, 10],
            ),
            [6, 7],
        ),
        (
            (
                [5, 6, 7],
                [0, 0, 0, 0, 5, 6, 7],
            ),
            [],
        ),
    ],
)
def test_also_available_in_column(input_data, expected):
    assert also_available_in_column(*input_data) == expected


def test_get_columns():
    puzzle1 = np.array(
        [
            [1, 2, 3, 4],
            [4, 3, 2, 1],
            [0, 0, 0, 0],
            [3, 2, 1, 0],
        ]
    )
    puzzle2 = np.array(
        [
            [1, 2, 3],
            [4, 3, 2],
            [0, 0, 0],
        ]
    )
    puzzle3 = np.array(
        [
            [1, 2, 3, 4, 5, 6],
            [4, 3, 2, 1, 0, 0],
            [0, 0, 0, 0, 1, 4],
            [3, 2, 1, 0, 6, 5],
            [0, 0, 0, 0, 3, 1],
            [0, 0, 1, 0, 0, 0],
        ]
    )
    expected_columns = [
        [
            [1, 4, 0, 3],
            [2, 3, 0, 2],
            [3, 2, 0, 1],
            [4, 1, 0, 0],
        ],
        [
            [1, 4, 0],
            [2, 3, 0],
            [3, 2, 0],
        ],
        [
            [1, 4, 0, 3, 0, 0],
            [2, 3, 0, 2, 0, 0],
            [3, 2, 0, 1, 0, 1],
            [4, 1, 0, 0, 0, 0],
            [5, 0, 1, 6, 3, 0],
            [6, 0, 4, 5, 1, 0],
        ],
    ]
    for puzzle, expected in zip([puzzle1, puzzle2, puzzle3], expected_columns):
        for col, exp_col in zip(get_columns(puzzle), expected):
            assert list(col) == exp_col


def test_solve():
    expected_4txt = np.array(
        [
            [4, 1, 3, 2],
            [2, 3, 1, 4],
            [3, 4, 2, 1],
            [1, 2, 4, 3],
        ]
    )

    parent = Path(__file__).parent.parent

    for path in [DATA4_TXT, DATA9_TXT, DATA16_TXT]:
        data_path = Path.joinpath(parent, path)
        puzzle = collect_puzzle(data_path)
        solved = solve(puzzle)

        if path == DATA4_TXT:
            assert np.array_equal(solved, expected_4txt)

        else:
            assert solved == []


def test_print_puzzle(monkeypatch):
    """Totally unnecessary."""

    import sys
    from io import StringIO

    mocked = StringIO()
    monkeypatch.setattr(sys, "stdout", mocked)

    parent = Path(__file__).parent.parent
    data_path = Path.joinpath(parent, DATA4_TXT)
    puzzle = collect_puzzle(data_path)

    print_puzzle(puzzle)
    for row, expected_row in zip(
        puzzle, mocked.getvalue().strip()[len("puzzle:") + 1 : :].split("\n")
    ):
        assert str(row) == expected_row
