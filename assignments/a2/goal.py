"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


def init_matrix(size: int) -> List[List[int]]:
    """Returns a <size> by <size> matrix whose entries are all -1.
    """
    m = []
    for i in range(size):
        m.append([])
        for _ in range(size):
            m[i].append(-1)
    return m


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A goal to create the most possible units of a given
    colour c on the outer perimeter of the board.
    """
    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """ Initalize a new PerimeterGoal.
        """
        Goal.__init__(self, target_colour)

    def description(self) -> str:
        """Return a description of the BlobGoal type.
        """
        return "Create the most possible " \
               "units on the outer perimeter of the board"

    def score(self, board: Block) -> int:
        """ Calculate and return the score associated with the most units on
        the outer perimeter on <board>. """
        s = 0
        rep = board.flatten()
        for i in range(0, len(rep)):
            if rep[i][0] == self.colour:
                s += 1
            if rep[0][i] == self.colour:
                s += 1
            if rep[len(rep) - 1][i] == self.colour:
                s += 1
            if rep[i][len(rep) - 1] == self.colour:
                s += 1

        return s


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """ Initialize a new BlobGoal.
        """
        Goal.__init__(self, target_colour)

    def description(self) -> str:
        """Return a description of the BlobGoal type.
        """
        return "Create the largest connected blob"

    def score(self, board: Block) -> int:
        """ Calculate and return the score associated with the largest connected
        blob on <board>. """
        mx_b = 0

        rep = board.flatten()
        size = len(rep)
        v = init_matrix(size)

        for i in range(size):
            for j in range(size):
                mx_b = max(mx_b, self._undiscovered_blob_size((i, j), rep, v))
        return mx_b

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that
        (a) is of this Goal's target colour,
        (b) includes the cell at <pos>, and
        (c) involves only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """

        out_of_bounds = pos[0] >= len(board[0]) or pos[0] < 0 or \
            pos[1] >= len(board[1]) or pos[1] < 0

        if out_of_bounds or visited[pos[0]][pos[1]] != -1:
            return 0
        elif board[pos[0]][pos[1]] != self.colour:  # Not of target colour
            visited[pos[0]][pos[1]] = 0
            return visited[pos[0]][pos[1]]
        else:   # unvisited target colour nodes
            visited[pos[0]][pos[1]] = 1

            # Recrusively find connected blobs up, down, left, + right of pos
            u = self._undiscovered_blob_size((pos[0]-1, pos[1]), board, visited)
            d = self._undiscovered_blob_size((pos[0]+1, pos[1]), board, visited)
            f = self._undiscovered_blob_size((pos[0], pos[1]-1), board, visited)
            r = self._undiscovered_blob_size((pos[0], pos[1]+1), board, visited)

            connected_blobs = u + d + f + r

            return 1 + connected_blobs


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
