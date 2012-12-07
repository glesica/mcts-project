% Playing Like a Gambler
% George Tiberius Lesica
% Fall 2012

# Monte Carlo Tree Search

  * Actually a family of algorithms
  * Stochastic tree search algorithm
  * Based on sampling outcome density

# What is it Used For?

Funny you should aks...

  * Go (smart people)
    * Complex game
    * No good heuristics
  * Connect Four (me)
    * Simple game
    * Analytically "solved"

# How Does it Work?

  * Magic... and ponies!

# Be Serious.

Fine.

~~~~
MCTS()
  Pick a child node
  Simulate the rest of the game randomly
  Note who won
  Repeat until bored
~~~~

# That's Crazy Like a Walrus.

Or is it crazy like a walrus-fox?

  * Algorithm makes intuituve sense
  * Game simulated to the end
  * Find action that is "most likely" to win

# So What Did You Do With It?

One word: Connect Four

  * Fixed maximum depth
  * Fairly high branching factor
  * Totally tree-like (no cycles)

# Is There a Sweet Demo?

  * Why yes, yes there is
