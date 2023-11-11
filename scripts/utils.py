"""Utility functions for coordinates and families of sets"""

# pylint: disable = invalid-name

from typing import TypeVar

T = TypeVar("T")


def rotate(coord: tuple[int, int]) -> tuple[int, int]:
    """Rotates a coordinate by 90° anti-clockwise"""
    x, y = coord
    return -y, x


def reflect(coord: tuple[int, int]) -> tuple[int, int]:
    """Reflects a coordinate horizontally"""
    x, y = coord
    return -x, y


def adjust(coords: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Shifts a set of coordinates so that they are non-negative
    and as small as possible
    """
    min_x = min(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    return {(x - min_x, y - min_y) for x, y in coords}


def valid_shift(
    coords: set[tuple[int, int]], shift: tuple[int, int], dim: tuple[int, int]
) -> bool:
    """Checks if a set of coordinates remains in a rectangle when shifted"""
    i, j = shift
    n, m = dim
    return all(0 <= x + i < n and 0 <= y + j < m for x, y in coords)


def get_amount(x: T, S: list[set[T]]) -> int:
    """Computes the amount of appearances of an element in a list of sets."""
    return len([A for A in S if x in A])


def get_least_common(X: set[T], S: list[set[T]]) -> tuple[T, int]:
    """Computes the least common element in a family of sets."""
    if len(X) == 0:
        raise ValueError("The list cannot be empty")
    least_amount = len(S)
    element = next(iter(X))
    for x in X:
        amount = get_amount(x, S)
        if least_amount is None or amount < least_amount:
            least_amount = amount
            element = x
    return (element, least_amount)
