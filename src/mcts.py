"""
An implementation of the MCTS algorithm.
"""


class Problem(object):
    def __init__(self, initial):
        self.initial = initial

    def actions(self, state):
        raise Exception('Method must be overridden.')

    def result(self, state, action):
        raise Exception('Method must be overridden.')

    def terminal(self, state):
        raise Exception('Method must be overridden.')


class ConnectFour(Problem):
    """
    Implementation of the game Connect Four, modeled as a tree search problem.
    The state is a tuple of tuples. The inner tuples represent columns in the
    game board. The first element in each corresponds to the bottom slot in the
    game board. If a slot is not occupied then it simply is not present in the
    state representation.
    """
    TARGET = 4
    VALUE_WIN = 1
    VALUE_LOSE = -1
    VALUE_DRAW = 0

    def __init__(self, initial, players=(1,2), width, height):
        Problem.__init__(self, initial)
        self.players  = players
        self.width    = width
        self.height   = height

    def _valid_action(self, state, action):
        index, _ = action
        return len(state[index]) < self.height

    def actions(self, state, player):
        return tuple(
            [(i, player) for i, _ in enumerate(state) if self._valid_action(state, (i, player))]
        )

    def result(self, state, action):
        if not self._valid_action(state, action):
            raise Exception('Invalid action.')
        index, player = action
        newstate = []
        for i, column in enumerate(state):
            if i == index:
                newstate.append(column + (player,))
            else:
                newstate.append(column)
        return tuple(newstate)

    def terminal(self, state):
        # All columns full means we are done
        if all([len(column) == self.height for column in state]):
            return True
        # A winner also means we are done
        if all([self.outcome(state, player) != self.VALUE_DRAW for player in self.players]):
            return True
        # Board is not full and no one has won so the game continues
        return False
        
    def outcome(self, state, player):
        # TODO: Improve the big fat constant associated with this method.
        def streak(state, player, start, delta, length=0, target=self.TARGET):
            # Streak is already long enough, done, success
            if length == target:
                return True
            # Streak has ended or run into edge, done, failure
            try:
                row, column = start
                if state[column][row] != player:
                    return False
            except IndexError:
                return False
            # Continue searching, current slot is owned by the player
            drow, dcolumn = delta
            return streak(
                state,
                player,
                (row + drow, column + dcolumn),
                delta,
                length + 1,
                target
            )
        for column, cells in enumerate(state):
            for row, p in enumerate(column):
                if any((
                    streak(state, p, (row, column), (-1, 0)),
                    stream(state, p, (row, column), (1, 0)),
                    stream(state, p, (row, column), (0, -1)),
                    stream(state, p, (row, column), (0, 1)),
                    stream(state, p, (row, column), (-1, 1)),
                    stream(state, p, (row, column), (1, 1)),
                    stream(state, p, (row, column), (1, -1)),
                    stream(state, p, (row, column), (-1, -1))
                )):
                    if player == p:
                        return self.VALUE_WIN
                    else:
                        return self.VALUE_LOSE
        # No winner was found, so game is a draw at the moment
        return self.VALUE_DRAW


class Node(object):
    def __init__(self, parent, state, action):
        self.parent   = parent
        self.state    = state
        self.action   = action
        self.weight   = 0.0
        self.visits   = 0


def mcts(problem):
    pass
