"""
Polynomino class, mainly used for creating all 12 pentominoes
and their rotations and reflections, being 63 in total
"""


from __future__ import annotations
import utils


class Polynomino:
    """Polynomino class"""

    def __init__(self, name: str, coords: set[tuple[int, int]]):
        """
        Initializer function, automatically adjusts the coordinates

        Arguments:
            name: name of the polynomino
            coords: set of coordinates, each being a tuple of two integers
        """
        self.coords = utils.adjust(coords)
        self.name = name

    def __str__(self) -> str:
        """Generates a reader-friendly representation of the polynomino"""
        output = ""
        max_x = max(x for x, _ in self.coords)
        max_y = max(y for _, y in self.coords)
        for i in range(max_x + 1):
            for j in range(max_y + 1):
                output += "X" if (i, j) in self.coords else " "
            output += "\n"
        return output

    def __eq__(self, other: object) -> bool:
        """Checks if two polynominoes are equal"""
        if not isinstance(other, Polynomino):
            return NotImplemented
        return self.coords == other.coords

    def rotate(self) -> Polynomino:
        """Creates a new polynomio with rotated coordinates"""
        rotated_coords = {utils.rotate(coord) for coord in self.coords}
        return Polynomino(self.name, rotated_coords)

    def reflect(self) -> Polynomino:
        """Creates a new polynomino with reflected coordinates"""
        reflected_coords = {utils.reflect(coord) for coord in self.coords}
        return Polynomino(self.name, reflected_coords)

    def variations(self) -> list[Polynomino]:
        """Creates a list of all variations of the polynomino"""
        list_of_variations: list[Polynomino] = []
        variation = self
        while variation not in list_of_variations:
            list_of_variations.append(variation)
            variation = variation.rotate()
        variation = self.reflect()
        while variation not in list_of_variations:
            list_of_variations.append(variation)
            variation = variation.rotate()
        return list_of_variations


LIST_PENTOMINOES = [
    Polynomino(name="F", coords={(0, 1), (0, 2), (1, 1), (1, 0), (2, 1)}),
    Polynomino(name="I", coords={(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)}),
    Polynomino(name="L", coords={(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)}),
    Polynomino(name="N", coords={(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)}),
    Polynomino(name="P", coords={(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)}),
    Polynomino(name="T", coords={(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)}),
    Polynomino(name="U", coords={(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)}),
    Polynomino(name="V", coords={(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}),
    Polynomino(name="W", coords={(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}),
    Polynomino(name="X", coords={(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)}),
    Polynomino(name="Y", coords={(1, 0), (0, 1), (1, 1), (2, 1), (3, 1)}),
    Polynomino(name="Z", coords={(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)}),
]
"""List of all 12 pentominoes"""


def main() -> None:
    """Prints all pentominoes and their variations"""
    total = 0
    for pentimono in LIST_PENTOMINOES:
        variations = pentimono.variations()
        total += len(variations)
        print(f"Pentomino {pentimono.name} variations ({len(variations)}):\n")
        for p in variations:
            print(p)
    print(f"In total, there are {total} variations")


if __name__ == "__main__":
    main()
