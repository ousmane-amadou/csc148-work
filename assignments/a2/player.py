"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the player class hierarchy.
"""

import random
from typing import Optional, Dict
import pygame
from renderer import Renderer
from block import Block
from goal import Goal

TIME_DELAY = 600


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    renderer:
        The object that draws our Blocky board on the screen
        and tracks user interactions with the Blocky board.
    id:
        This player's number.  Used by the renderer to refer to the player,
        for example as "Player 2"
    goal:
        This player's assigned goal for the game.
    """
    renderer: Renderer
    id: int
    goal: Goal

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.renderer = renderer
        self.id = player_id

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        raise NotImplementedError

class SmartPlayer(Player):
    """A player in the Blocky game.

       This is an abstract class. Only child classes should be instantiated.

       === Public Attributes ===
       renderer:
           The object that draws our Blocky board on the screen
           and tracks user interactions with the Blocky board.
       id:
           This player's number.  Used by the renderer to refer to the player,
           for example as "Player 2"
       goal:
           This player's assigned goal for the game.
       """
    difficulty: int
    board_state: GameState
    move_memory: Dict[GameState, MoveHeap]

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal, difficulty: int) -> None:
        """"""
        super().__init__(renderer, player_id, goal)
        self.difficulty = difficulty

        self.board_state = None
        self.move_memory = {}

    def make_move(self, board: Block):
        """Choose the best move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Number of moves compared depends on set difficulty:
        0 = 5
        1 = 10
        2 = 25
        3 = 50
        4 = 100
        >= 5 = 150
        """
        num_moves = 0
        move_breadth = 0

        moves_legend = {0: 5, 1: 10, 2: 25, 3: 50, 4: 100}
        if self.difficulty >= 5:
            num_moves = 150
        else:
            num_moves = moves_legend[self.difficulty]

        # Prep: Update Current State of board, and add it to memory
        board_state = GameState(board, self.goal.score(board))
        self._add_state(board_state)

        # First: Generate 'n' new moves, and
        # add the associated states and moves to memory
        self._generate_moves(num_moves, move_breadth)

        # Second: Get the next best move, from memory
        my_move = self._get_next_move()

        # Select block that is to be moved
        my_move.move_block.highlighted = True

        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)

        # Third: Execute the move
        if my_move.move_type == 0:   # Rotate the selected block either clockwise or counter clock wise
            my_move.move_block.rotate(1)
        elif my_move.move_type == 1:   # Rotate the selected block either clockwise or counter clock wise
            my_move.move_block.rotate(3)
        elif my_move.move_type == 2: # Swap the 4 sub blocks within the selcted block horizontally or vertically
            my_move.move_block.rotate(0)
        elif my_move.move_type == 3:
            my_move.move_block.swap(1)

        my_move.move_block.highlighted = False
        self.renderer.draw(board.rectangles_to_draw(), self.id)

    def wipe_memory(self):
        """
        """
        self.move_memory = {}

    def _add_state(self, board_state: GameState) -> int:
        """ Add board_state to move_memory, if board_state isnt already in memory.
        Otherwise, return 0.
        """
        if board_state in self.move_memory:
            return 0
        else:
            self.move_memory[board_state] = MoveHeap()
            return 1

    def _add_move(self, move: Move) -> int:
        if move.start_state in self.move_memory:
            self.move_memory[move.start_state].insert(move)
            self.move_memory[move.end_state].insert(move)
            return 0
        else:
            self.move_memory[move.start_state] = MoveHeap()
            self.move_memory[move.end_state] = MoveHeap()

            self.move_memory[move.start_state].insert(move)
            self.move_memory[move.end_state].insert(move)
            return 1

    def _get_next_move(self):
        return self.move_memory[self.board_state].getBestMove()

    def _generate_move(self) -> Move:

    def _grow_move_memory(self, num_moves: int, move_breadth: int):
        """ Add <num_moves> more moves to the move_memory. Limit the number
        of moves generated per state (or turn) to <move_breadth>.
        """
        moves_added = 0
        state_stk = [self.board_state]
        while state_stk and moves_added <= num_moves:
            state = state_stk.pop()

            state_move_count = self.move_memory[state].size()

            while state_move_count < move_breadth:
                m = self._generate_move()
                familar_end_state = self._add_move(m)
                state_move_count += 1

                if not familar_end_state:
                    state_stk.append(m.end_state)


class MoveHeap:
    pass

class GameState:
    """

    """
    board: Block
    score: int

    def __init__(self, board: Block, score: int):
        self.board = board
        self.score = score

class Move:
    """

    """
    start_state: GameState
    end_state: GameState
    move_type: int
    move_block: Block

    def __init__(self, start_state: GameState, end_state: GameState,
                       move_type: int, move_block: Block):
        self.start_state = start_state
        self.end_state = end_state
        self.move_type = move_type
        self.move_block = move_block

class RandomPlayer(Player):
    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """"""
        super().__init__(renderer, player_id, goal)

    def make_move(self, board: Block):
        # Choose Random block
        random_loc = (random.randint(0, board.size), random.randint(0, board.size))
        random_level = random.randint(1, board.max_depth)

        move_block = board.get_selected_block(random_loc, random_level)
        move_block.highlighted = True

        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)

        random_action = random.randint(0, 4)

        if random_action == 0:   # Rotate the selected block either clockwise or counter clock wise
            move_block.rotate(1)
        elif random_action == 1:
            move_block.rotate(3)
        elif random_action == 2: # Swap the 4 sub blocks within the selcted block horizontally or vertically
            move_block.swap(0)
        elif random_action == 3:
            move_block.swap(1)
        elif random_action == 4:
            move_block.smash(random.randint(0, move_block.max_depth))

        move_block.highlighted = False
        self.renderer.draw(board.rectangles_to_draw(), self.id)


class HumanPlayer(Player):
    """A human player.

    A HumanPlayer can do a limited number of smashes.

    === Public Attributes ===
    num_smashes:
        number of smashes which this HumanPlayer has performed
    === Representation Invariants ===
    num_smashes >= 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the user has most recently selected for action;
    #     changes upon movement of the cursor and use of arrow keys
    #     to select desired level.
    # _level:
    #     The level of the Block that the user selected
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0

    # The total number of 'smash' moves a HumanPlayer can make during a game.
    MAX_SMASHES = 1

    num_smashes: int
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self.num_smashes = 0

        # This HumanPlayer has done no smashes yet.
        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._selected_block = None

    def process_event(self, board: Block,
                      event: pygame.event.Event) -> Optional[int]:
        """Process the given pygame <event>.

        Identify the selected block and mark it as highlighted.  Then identify
        what it is that <event> indicates needs to happen to <board>
        and do it.

        Return
           - None if <event> was not a board-changing move (that is, if was
             a change in cursor position, or a change in _level made via
            the arrow keys),
           - 1 if <event> was a successful move, and
           - 0 if <event> was an unsuccessful move (for example in the case of
             trying to smash in an invalid location or when the player is not
             allowed further smashes).
        """

        # Get the new "selected" block from the position of the cursor
        block = board.get_selected_block(pygame.mouse.get_pos(), self._level)

        # Remove the highlighting from the old "_selected_block"
        # before highlighting the new one
        if self._selected_block is not None:
            self._selected_block.highlighted = False
        self._selected_block = block
        self._selected_block.highlighted = True

        # Since get_selected_block may have not returned the block at
        # the requested level (due to the level being too low in the tree),
        # set the _level attribute to reflect the level of the block which
        # was actually returned.
        self._level = block.level

        if event.type == pygame.MOUSEBUTTONDOWN:
            block.rotate(event.button)
            return 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if block.parent is not None:
                    self._level -= 1
                return None

            elif event.key == pygame.K_DOWN:
                if len(block.children) != 0:
                    self._level += 1
                return None

            elif event.key == pygame.K_h:
                block.swap(0)
                return 1

            elif event.key == pygame.K_v:
                block.swap(1)
                return 1

            elif event.key == pygame.K_s:
                if self.num_smashes >= self.MAX_SMASHES:
                    print('Can\'t smash again!')
                    return 0
                if block.smash(board.max_depth):
                    self.num_smashes += 1
                    return 1
                else:
                    print('Tried to smash at an invalid depth!')
                    return 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.
        """
        self._level = 0
        self._selected_block = board

        # Remove all previous events from the queue in case the other players
        # have added events to the queue accidentally.
        pygame.event.clear()

        # Keep checking the moves performed by the player until a valid move
        # has been completed. Draw the board on every loop to draw the
        # selected block properly on screen.
        while True:
            self.renderer.draw(board, self.id)
            # loop through all of the events within the event queue
            # (all pending events from the user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1

                result = self.process_event(board, event)
                self.renderer.draw(board, self.id)
                if result is not None and result > 0:
                    # un-highlight the selected block
                    self._selected_block.highlighted = False
                    return 0


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer',
            'pygame'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
