"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Block class, the main data structure used in the game.
"""
from typing import Optional, Tuple, List
import random
import math
from renderer import COLOUR_LIST, TEMPTING_TURQUOISE, BLACK


HIGHLIGHT_COLOUR = TEMPTING_TURQUOISE
FRAME_COLOUR = BLACK


def init_matrix(size: int) -> List[List[int]]:
    """Returns a <size> by <size> matrix whose entries are all -1.
    """
    m = []
    for i in range(size):
        m.append([])
        for _ in range(size):
            m[i].append(-1)
    return m


class Block:
    """A square block in the Blocky game.

    === Public Attributes ===
    position:
        The (x, y) coordinates of the upper left corner of this Block.
        Note that (0, 0) is the top left corner of the window.
    size:
        The height and width of this Block.  Since all blocks are square,
        we needn't represent height and width separately.
    colour:
        If this block is not subdivided, <colour> stores its colour.
        Otherwise, <colour> is None and this block's sublocks store their
        individual colours.
    level:
        The level of this block within the overall block structure.
        The outermost block, corresponding to the root of the tree,
        is at level zero.  If a block is at level i, its children are at
        level i+1.
    max_depth:
        The deepest level allowed in the overall block structure.
    highlighted:
        True iff the user has selected this block for action.
    children:
        The blocks into which this block is subdivided.  The children are
        stored in this order: upper-right child, upper-left child,
        lower-left child, lower-right child.
    parent:
        The block that this block is directly within.

    === Representation Invariations ===
    - len(children) == 0 or len(children) == 4
    - If this Block has children,
        - their max_depth is the same as that of this Block,
        - their size is half that of this Block,
        - their level is one greater than that of this Block,
        - their position is determined by the position and size of this Block,
          as defined in the Assignment 2 handout, and
        - this Block's colour is None
    - If this Block has no children,
        - its colour is not None
    - level <= max_depth
    """
    position: Tuple[int, int]
    size: int
    colour: Optional[Tuple[int, int, int]]
    level: int
    max_depth: int
    highlighted: bool
    children: List['Block']
    parent: Optional['Block']

    def __init__(self, level: int,
                 colour: Optional[Tuple[int, int, int]] = None,
                 children: Optional[List['Block']] = None) -> None:
        """Initialize this Block to be an unhighlighted root block with
        no parent.

        If <children> is None, give this block no children.  Otherwise
        give it the provided children.  Use the provided level and colour,
        and set everything else (x and y coordinates, size,
        and max_depth) to 0.  (All attributes can be updated later, as
        appropriate.)
        """
        self.highlighted = False
        self.parent = None

        self.level = level
        self.colour = colour
        self.children = [] if children is None else children

        self.position = (0, 0)
        self.size = 0
        self.max_depth = 0

    def rectangles_to_draw(self) -> List[Tuple[Tuple[int, int, int],
                                               Tuple[float, float],
                                               Tuple[float, float],
                                               int]]:
        """
        Return a list of tuples describing all of the rectangles to be drawn
        in order to render this Block.

        This includes (1) for every undivided Block:
            - one rectangle in the Block's colour
            - one rectangle in the FRAME_COLOUR to frame it at the same
              dimensions, but with a specified thickness of 3
        and (2) one additional rectangle to frame this Block in the
        HIGHLIGHT_COLOUR at a thickness of 5 if this block has been
        selected for action, that is, if its highlighted attribute is True.

        The rectangles are in the format required by method Renderer.draw.
        Each tuple contains:
        - the colour of the rectangle
        - the (x, y) coordinates of the top left corner of the rectangle
        - the (height, width) of the rectangle, which for our Blocky game
          will always be the same
        - an int indicating how to render this rectangle. If 0 is specified
          the rectangle will be filled with its colour. If > 0 is specified,
          the rectangle will not be filled, but instead will be outlined in
          the FRAME_COLOUR, and the value will determine the thickness of
          the outline.

        The order of the rectangles does not matter.
        """
        d = []

        if self.children == []:
            d += [(self.colour, self.position, (self.size, self.size), 0)]
            d += [(FRAME_COLOUR, self.position, (self.size, self.size), 3)]
        else:
            for i in range(len(self.children)):
                d += self.children[i].rectangles_to_draw()

        if self.highlighted:
            d += [(HIGHLIGHT_COLOUR, self.position, (self.size, self.size), 5)]

        return d

    def swap(self, direction: int) -> None:
        """Swap the child Blocks of this Block.

        If <direction> is 1, swap vertically.  If <direction> is 0, swap
        horizontally. If this Block has no children, do nothing.
        """
        if self.children == []:
            pass
        else:
            if direction == 1:
                self.children = [self.children[3], self.children[2],
                                 self.children[1], self.children[0]]
            elif direction == 0:
                self.children = [self.children[1], self.children[0],
                                 self.children[3], self.children[2]]

            self.update_block_locations(self.position, self.size)

    def rotate(self, direction: int) -> None:
        """Rotate this Block and all its descendants.

        If <direction> is 1, rotate clockwise.  If <direction> is 3, rotate
        counterclockwise. If this Block has no children, do nothing.
        """
        if len(self.children) == 0:
            pass
        else:
            if direction == 3:
                self.children = [self.children[3], self.children[0],
                                 self.children[1], self.children[2]]
            elif direction == 1:
                self.children = [self.children[1], self.children[2],
                                 self.children[3], self.children[0]]
            else:
                return

            for i in range(4):
                self.children[i].rotate(direction)

            self.update_block_locations(self.position, self.size)

    def smash(self) -> bool:
        """Smash this block.

        If this Block can be smashed,
        randomly generating four new child Blocks for it.  (If it already
        had child Blocks, discard them.)
        Ensure that the RI's of the Blocks remain satisfied.

        A Block can be smashed iff it is not the top-level Block and it
        is not already at the level of the maximum depth.

        Return True if this Block was smashed and False otherwise.
        """

        if 0 < self.level < self.max_depth:
            self.children = []
            for _ in range(4):
                self.children.append(random_init(self.level + 1,
                                                 self.max_depth))
            self.update_block_locations(self.position, self.size)
            return True
        else:
            return False

    def update_block_locations(self, top_left: Tuple[float, float],
                               size: float) -> None:
        """
        Update the position and size of each of the Blocks within this Block.

        Ensure that each is consistent with the position and size of its
        parent Block.

        <top_left> is the (x, y) coordinates of the top left corner of
        this Block.  <size> is the height and width of this Block.
        """
        if self.children == []:
            pass
        else:
            self.size = size
            for i in range(len(self.children)):
                child = self.children[i]
                child.size = round(size / 2.0)

                # Sets x position for child
                # Modify x position if child is top-right, bottom-right
                child_x = top_left[0] + ((i == 0) | (i == 3)) * child.size

                # Sets y position for child
                # Modify y position if child is bottom-left, bottom-right
                child_y = top_left[1] + ((i == 2) | (i == 3)) * child.size

                child.position = (child_x, child_y)
                child.update_block_locations(child.position, child.size)

    def get_selected_block(self, location: Tuple[float, float], level: int) \
            -> 'Block':
        """Return the Block within this Block that includes the given location
        and is at the given level. If the level specified is lower than
        the lowest block at the specified location, then return the block
        at the location with the closest level value.

        <location> is the (x, y) coordinates of the location on the window
        whose corresponding block is to be returned.
        <level> is the level of the desired Block.  Note that
        if a Block includes the location (x, y), and that Block is subdivided,
        then one of its four children will contain the location (x, y) also;
        this is why <level> is needed.

        Preconditions:
        - 0 <= level <= max_depth
        """
        if self.children == []:
            return self
        elif level == 0:
            return self
        else:
            selected_child = 0
            size = round(self.size / 2.0)
            left_child = location[0] < (self.position[0] + size)
            upper_child = location[1] < (self.position[1] + size)

            if left_child and upper_child:
                selected_child = 1
            elif left_child and not upper_child:
                selected_child = 2
            elif not upper_child and not left_child:
                selected_child = 3

            return self.children[selected_child].get_selected_block(
                location, level-1)

    def flatten(self) -> List[List[Tuple[int, int, int]]]:
        """Return a two-dimensional list representing this Block as rows
        and columns of unit cells.

        Return a list of lists m, where, for 0 <= i, j < 2^{self.level}
            - m[i] represents column i and
            - m[i][j] represents the unit cell at column i and row j.
        Each unit cell is represented by 3 ints for the colour
        of the block at the cell location[i][j]

        m[0][0] represents the unit cell in the upper left corner of the Block.
        """
        units = 2 ** (self.max_depth - self.level)
        sub_unit = int(math.floor(units/2))
        m = init_matrix(units)

        if self.children == []:
            m = [[self.colour for _ in range(units)] for _ in range(units)]
        else:
            # Recusively flatten children
            mtr = self.children[0].flatten()
            mtl = self.children[1].flatten()
            mbl = self.children[2].flatten()
            mbr = self.children[3].flatten()

            for i in range(units):
                for j in range(units):
                    if (i < sub_unit) and (j < sub_unit):
                        m[i][j] = mtl[i][j]
                    elif (i < sub_unit) and (j >= sub_unit):
                        m[i][j] = mbl[i][j-sub_unit]
                    elif (i >= sub_unit) and (j < sub_unit):
                        m[i][j] = mtr[i-sub_unit][j]
                    else:
                        m[i][j] = mbr[i-sub_unit][j-sub_unit]

        return m


def random_init(level: int, md: int) -> 'Block':
    """Return a randomly-generated Block with level <level> and subdivided
    to a maximum depth of <max_depth>.

    Throughout the generated Block, set appropriate values for all attributes
    except position and size.  They can be set by the client, using method
    update_block_locations.

    Precondition:
        level <= max_depth
    """
    # If this Block is not already at the maximum allowed depth, it can
    # be subdivided. Use a random number to decide whether or not to
    # subdivide it further.

    if level < md and random.random() <= math.exp(-0.25 * level):
        b = Block(level, children=[random_init(level+1, md) for _ in range(4)])

        # Set parent attribute for each child block
        for child in b.children:
            child.parent = b
    else:
        b = Block(level, random.choice(COLOUR_LIST), children=None)

    b.max_depth = md    # Set max_depth attribute for current block
    return b


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer', 'math'
        ],
        'max-attributes': 15
    })
