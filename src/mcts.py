"""
A collection of classes and functions for playing certain types of
games. Specifically, an implementation of the MCTS algorithm.
"""
import random, Queue


class Game(object):
    """
    Base class for multi-player adversarial games.
    """
    def actions(self, state):
        raise Exception('Method must be overridden.')

    def result(self, state, action, player):
        raise Exception('Method must be overridden.')

    def terminal(self, state):
        raise Exception('Method must be overridden.')

    def next_player(self, player):
        raise Exception('Method must be overridden.')

    def outcome(self, state, player):
        raise Exception('Method must be overridden.')


class ConnectFour(Game):
    """
    Implementation of the game Connect Four, modeled as a tree search problem.

    The state is a tuple of tuples. The last element is the player whose turn
    it is, the rest of the elements are tuples that represent columns in the
    game board. The first element in each corresponds to the bottom slot in the
    game board. If a slot is not occupied then it simply is not present in the
    state representation.

    ( (), (), (), (), 1 ) Four empty columns, player 1's turn

    An action is just an integer representing a column in the game board
    (state). The player is taken from the state and the move is attributed to
    this player.
    """
    PLAYERS = (1,2)
    HEIGHT = 4
    WIDTH = 4

    TARGET = 3

    VALUE_WIN = 1
    VALUE_LOSE = -1
    VALUE_DRAW = 0

    def __init__(self, players=PLAYERS, height=HEIGHT, width=WIDTH, target=TARGET):
        self.players  = players
        self.height   = height
        self.width    = width
        self.target   = target

    def _legal(self, state, action):
        if action not in xrange(len(state)):
            raise Exception('Invalid action: out of range')
        return len(state[action]) < self.height

    def _streak(self, state, player, start, delta, length=0, target=None):
        # TODO: Clean up length/target, don't need both, just use self.target
        # Set the default target length if we weren't given one
        if target is None:
            target = self.target
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
        return self._streak(
            state,
            player,
            (row + drow, column + dcolumn),
            delta,
            length + 1,
            target
        )

    def pretty_state(self, state, escape=True):
        output = ''
        i = self.height - 1
        while i >= 0:
            for column in state:
                if len(column) > i:
                    output += str(column[i])
                else:
                    output += 'E'
            if escape:
                output += '\\n'
            else:
                output += '\n'
            i -= 1
        return output

    def actions(self, state):
        return tuple(
            [i for i, _ in enumerate(state) if self._legal(state, i)]
        )

    def result(self, state, action, player):
        if not self._legal(state, action):
            raise Exception('Illegal action')
        newstate = []
        for index, column in enumerate(state):
            if index == action:
                newstate.append(column + (player,))
            else:
                newstate.append(column)
        return tuple(newstate)

    def terminal(self, state):
        # All columns full means we are done
        if all([len(column) == self.height for column in state]):
            return True
        # A winner also means we are done
        if self.outcome(state, self.players[0]) != self.VALUE_DRAW:
            return True
        # Board is not full and no one has won so the game continues
        return False

    def next_player(self, player):
        if player not in self.players:
            raise Exception('Invalid player')
        index = self.players.index(player)
        if index < len(self.players) - 1:
            return self.players[index + 1]
        else:
            return self.players[0]
        
    def outcome(self, state, player):
        for ci, column in enumerate(state):
            for ri, marker in enumerate(column):
                if any((
                    self._streak(state, marker, (ri, ci), (1, 0)),
                    self._streak(state, marker, (ri, ci), (0, 1)),
                    self._streak(state, marker, (ri, ci), (1, 1)),
                    self._streak(state, marker, (ri, ci), (1, -1)),
                )):
                    # A winner was found
                    if marker == player:
                        return self.VALUE_WIN
                    else:
                        return self.VALUE_LOSE
        # No winner was found
        return self.VALUE_DRAW


class Node(object):

    COLORS = {
        1: 'red',
        2: 'yellow',
        3: 'orange',
        4: 'green',
        5: 'blue',
        6: 'purple'
    }

    def __init__(self, parent, action, state, player):
        # Structure
        self.parent    = parent
        self.children  = {}
        # Tree data
        self.action    = action
        self.state     = state
        # Search meta data
        self.player    = player
        self.visits    = 0
        self.value     = 0.0
    
    def __iter__(self):
        """
        A generator function. Does a pre-order traversal over the nodes
        in the tree without using recursion.
        """
        active = Queue.Queue()
        active.put(self)
        while active.qsize() > 0:
            next = active.get()
            for _, child in next.children.items():
                active.put(child)
            yield next

    def __len__(self):
        """
        Returns the number of nodes in the tree. This requires a
        traversal, so it has O(n) running time.
        """
        n = 0
        for node in self.traverse():
            n += 1
        return n
        
    def dot_string(self, value=False, prettify=lambda x: x):
        """
        Returns the tree rooted at the current node as a string
        in dot format. Each node is labeled with its state, which
        is first run through prettify. If value is True, then
        the value is included in the node label.
        """
        output = ''
        output += 'digraph {\n'
        for node in self:
            # Define the node
            name = prettify(node.state)
            if value:
                name += '%s\\n' % node.value
            color = self.COLORS[node.player]
            output += '\t"%s" [style="filled", fillcolor="%s"]\n' % (
                name, color
            )
            # No edge into the root node
            if node.parent is None:
                continue
            # Add edge from node parent to node
            pname = prettify(node.parent.state)
            if value:
                pname += '%s\\n' % node.parent.value
            output += '\t"%s" -> "%s"\n' % (pname, name)
        output += '}'
        return output


def full_tree(game, state, player):
    """
    Creates a full game tree in which player moves first. The traversal is done
    in breadth-first order. The return value is the root node.
    """
    active = Queue.Queue()
    root = Node(None, None, state, player)
    active.put(root)
    
    current = None
    while active.qsize() > 0:
        current = active.get()
        # Assign value if this is a terminal node
        if game.terminal(current.state):
            continue
        # Explore children otherwise
        for action in game.actions(current.state):
            nstate = game.result(current.state, action, current.player)
            nplayer = game.next_player(current.player)
            node = Node(current, action, nstate, nplayer)
            current.children[action] = node
            active.put(node)
    return root


def minimax(game, state, player):
    """
    Applies the Minimax algorithm to the given game. Returns the
    root node with values assigned to each node in the game tree.
    """
    active = []
    
    root = full_tree(game, state, player)
    for node in root:
        active.append(node)
    
    current = None
    while active:
        current = active.pop()
        # Leaf (terminal) node
        if game.terminal(current.state):
            current.value = game.outcome(current.state, player)
            continue
        # Interior or root node
        values = tuple([i.value for i in current.children.values()])
        if current.player == player:
            current.value = max(values)
        else:
            current.value = min(values)
    
    return root


def mcts(game, state, player, n):
    """
    Implementation of the Monte Carlo Tree Search algorithm.
    """
    root = Node(None, None, state, player)
    unexplored = Queue.Queue()
    unexplored.put(root)

    for _ in xrange(n):
        # Quit early if we are out of nodes
        if unexplored.qsize() == 0:
            break
        # Add the new node to the tree
        current = unexplored.get()
        if current.parent is not None:
            current.parent.children[current.action] = current
        # Add the newly discovered nodes to the queue
        for action in game.actions(current.state):
            nstate = game.result(current.state, action, current.player)
            nplayer = game.next_player(current.player)
            node = Node(current, action, nstate, nplayer)
            unexplored.put(node)
        # Simulate the rest of the game from the current node
        cstate = current.state
        cplayer = current.player
        while not game.terminal(cstate):
            caction = random.choice(game.actions(cstate))
            cstate = game.result(cstate, caction, cplayer)
            cplayer = game.next_player(cplayer)
        simvalue = game.outcome(cstate, player)
        # Back simulation value up to the root
        backup = current
        while backup is not None:
            backup.value = (backup.value * backup.visits + simvalue) / (backup.visits + 1)
            backup.visits += 1
            backup = backup.parent

    return root








