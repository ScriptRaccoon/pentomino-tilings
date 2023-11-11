"""
Uses the exact cover algorithm to determine all pentomino tilings of
a rectangle where every one of the 12 pentomino tilings has to appear
exactly once. The possible rectangle sizes are 3x20, 4x15, 5x12, 6x10.
The results are saved as JSON files to the /data subfolder
"""

# pylint: disable = invalid-name

import json
from collections.abc import Iterator
from polynomino import LIST_PENTOMINOES
from exactcover import exactcovers
import utils


n, m = 4, 15
"""Dimension of the rectangle"""

assert n >= 3 and m >= 3 and n * m == 60

COORDINATES = {(i, j) for i in range(n) for j in range(m)}
"""Set of coordinates of the rectangle"""


def get_constraints() -> set[str]:
    """
    The constraints are the coordinates (i,j) of the rectangle,
    encoded as strings i|j, as well as the names of the pentominoes.
    """
    return {f"{i}|{j}" for i, j in COORDINATES}.union(
        {p.name for p in LIST_PENTOMINOES}
    )


def get_choices() -> Iterator[set[str]]:
    """
    The choices are the sets {N, i|j, ...} where N is the name of a
    pentomino, potentially rotated and/or reflected, and i|j,...
    are its coordinates, as long as they fit into the rectangle.
    """
    for p in LIST_PENTOMINOES:
        for q in p.variations():
            for i, j in COORDINATES:
                if utils.valid_shift(q.coords, (i, j), (n, m)):
                    yield {f"{y+i}|{x+j}" for y, x in q.coords}.union({p.name})


def transform_tiling(tiling: list[set[str]]) -> dict[str, list[tuple[int, int]]]:
    """
    The exact cover algorithm returns a list of sets, each one having the form
    {N, i|j, ...}. We transform such a tiling to a dictionary with entries
    N : {(i,j),...}
    """
    transform: dict[str, list[tuple[int, int]]] = {}
    for tile in tiling:
        name = next(filter(lambda x: len(x) == 1, tile))
        if not name:
            continue
        transform[name] = []
        for coord in tile:
            if len(coord) == 1:
                continue
            splitted = coord.split("|")
            if (
                len(splitted) == 2
                and splitted[0].isnumeric()
                and splitted[1].isnumeric()
            ):
                transform[name].append((int(splitted[0]), int(splitted[1])))
    return transform


def get_tilings() -> Iterator[dict[str, list[tuple[int, int]]]]:
    """
    Generator containing all pentomino tilings of a rectangle of size n x m
    where each pentomino name appears exactly once. They are determined using
    the exact cover algorithm.
    """
    X = get_constraints()
    S = list(get_choices())
    return map(transform_tiling, exactcovers(X, S))


def print_tiling_to_console(tiling: dict[str, list[tuple[int, int]]]) -> None:
    """Prints a tiling to the console, where each pentomino is printed with its name"""
    board = [["" for _ in range(m)] for _ in range(n)]
    for name, coords in tiling.items():
        for y, x in coords:
            board[y][x] = name
    for row in board:
        print(" ".join(row))
    print()


def print_tilings() -> None:
    """Prints each tiling and waits for input to generate the next one"""
    for tiling in get_tilings():
        print_tiling_to_console(tiling)
        input()


def save_tilings() -> None:
    """Compute the list of all tilings (takes a while) and saves them as JSON file"""
    tilings = list(get_tilings())
    with open(f"../public/data/tilings-{n}-{m}.json", "w", encoding="utf8") as file:
        json.dump(tilings, file)


if __name__ == "__main__":
    # print_tilings()
    save_tilings()
