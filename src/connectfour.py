import mcts

def play(human=True, n=1000):
# Testing ConnectFour - mcts()
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
            result = mcts.mcts(game, state, player, n)
            state = game.result(state, result.max_child().action, player)

        # Intermediate win check
        if game.terminal(state):
            break

        # Computer plays now
        result = mcts.mcts(game, state, computer, n)
        state = game.result(state, result.max_child().action, computer)

    print game.terminal(state)
    print game.outcome(state, player)

    game.pretty_state(state)
    outcome = game.outcome(state, player)
    if outcome == 1:
        print 'Player 1 wins.'
    elif outcome == -1:
        print 'Player 2 wins.'
    else:
        print 'Tie game.'

    return result

outcome = play(False)

