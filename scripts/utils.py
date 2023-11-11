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


def reducing_sets(X: set[T], S: list[set[T]]) -> list[set[T]]:
    """
    Computes the element x that is the least common element in the
    sets in S and returns the sets in S that contain x
    """
    containment_dict: dict[T, list[set[T]]] = {x: [] for x in X}
    for A in S:
        for x in A:
            containment_dict[x].append(A)

    return min(containment_dict.values(), key=len)
