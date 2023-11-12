"""
Algorithm to solve the exact cover problem,
implemented with sets instead of 0,1-matrices.
References:
https://en.wikipedia.org/wiki/Exact_cover
https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X
"""

# pylint: disable = invalid-name

from collections.abc import Iterator
from typing import TypeVar
import utils

T = TypeVar("T")


def exactcovers(
    X: set[T], S: list[set[T]], check_sanity=True
) -> Iterator[list[set[T]]]:
    """
    Solutions to the exact cover problem, where X is a set ("contstraints")
    and S is a set of subsets of X ("choices"). We encode S with a list
    of sets since Python does not allow sets of sets without hacks.

    Arguments:
        X: any finite set (whose elements have type T)
        S: any list of subsets of X
    Returns:
        Generator of all partitions of X that consist of sets in S.
    Raises:
        ValueError: When S does not consist of subsets of X
    """
    if check_sanity and not all(A.issubset(X) for A in S):
        raise ValueError("S needs to consist of subsets of X")
    if len(X) == 0:
        yield []
        return
    for A in utils.reducing_sets(X, S):
        Y = X.difference(A)
        F = [B for B in S if A.isdisjoint(B)]
        for cover in exactcovers(Y, F, False):
            yield [A] + cover


def main() -> None:
    """Prints the solutions to a concrete exact cover problem"""
    X = {1, 2, 3, 4, 5, 6, 7}

    S = [
        {1},
        {3},
        {7},
        {1, 2},
        {2, 3},
        {1, 3},
        {1, 2, 7},
        {4, 5, 6},
        {1, 2, 3},
        {3, 4, 5, 6},
    ]

    print("X =", X)
    print("S =", S)

    covers = exactcovers(X, S)
    count = 0

    print("Covers:")

    for cover in covers:
        count += 1
        print(cover)

    assert count == 6


if __name__ == "__main__":
    main()
