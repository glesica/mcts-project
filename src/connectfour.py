import sys
import mcts

def play(human=True, n=1000):
# Testing ConnectFour - mcts_uct()
    height = 6
    width = 7
    target = 4
    initial = ((),) * width

    game = mcts.ConnectFour(height=height, width=width, target=target)
    state = initial
    player = game.players[0]
    computer = game.players[1]

    while not game.terminal(state):
        print game.pretty_state(state, False)
        if human:
            prompt = 'Choose a move, choices are %s:' % (game.actions(state),)
            success = False
            while not success:
                choice = raw_input(prompt)
                try:
                    action = int(choice)
                    success = True
                except ValueError:
                    pass
            # Got a valid action
            state = game.result(state, action, player)
        else:
            action = mcts.mcts_uct(game, state, player, n)
            state = game.result(state, action, player)

        print 'Player 1 chose %s' % action
        print game.pretty_state(state, False)

        # Intermediate win check
        if game.terminal(state):
            break

        # Computer plays now
        action = mcts.mcts_uct(game, state, computer, n)
        state = game.result(state, action, computer)

        print 'Player 2 chose %s' % action

    print game.pretty_state(state, False)
    print
    outcome = game.outcome(state, player)
    if outcome == 1:
        print 'Player 1 wins.'
    elif outcome == -1:
        print 'Player 2 wins.'
    else:
        print 'Tie game.'
    

if len(sys.argv) > 1:
    n = int(sys.argv[1])
else:
    n = 1000

play(n=n)


