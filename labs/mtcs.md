# Monte-Carlo Tree Search

[Link to my fork](https://github.com/OliFryser/aigs)

## Alpha-beta with heuristic

Starting the lab by implementing a heuristic for mini-max gave me a good intuition for how one can evaluate an incomplete boardstate. My heuristic function puts greater value towards center positions, meaning the heuristic adds more to the evaluation for each of the player's pieces close to the center. Contrarily, it subtracts from the evalutaion for each of the opponent's pieces close to the center. The intution behind this, is that the center provides the most opportunities for 4 in a row.

Using alpha-beta pruning further allowed me to discard branches that *could not* be the best move. This made the AI quite good, and I was not able to beat it. I learned that by using a heuristic and alpha-beta pruning, one is able to create quite fast search-based opponents in a game with a more complex game than tic-tac-toe.

## Monte-Carlo

The hands-on experience of implementing the Monte-Carlo Tree Search algorithm taught gave me a better understanding of the different parts of the algorithm. It seems a little intimidating at first, but by following the pseudocode in one of the papers, I was able to implement it quite quickly. After ironing out some mistakes, it plays pretty well, though I will argue, not as well as my alpha-beta search.
