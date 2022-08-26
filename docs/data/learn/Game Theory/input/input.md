`{title} Game Theory`

```{toc}
```

# Terminology

 * `{bm} game theory` - A formal language for the representation and analysis of interactive situations where several players take actions that jointly determine the final outcome. `{ref} gt:p11` `{ref} gt:p18`

 * `{bm} player` - An agent that acts purposefully and logically to get as close as possible to a set of well-defined goals. What a player is depends on the context. For example, in the context of ...
 
   * economic behaviour, a player is a human.
   * molecular biology, a player may be a pathogenic bacteria, immune cell, virus, etc..
   * computer simulations, a player is typically an artificial agent.
   
   `{ref} gt:p11`

 * `{bm} cooperative game theory` - A branch of game theory where players can cooperate through communication, forming coalitions, and making binding agreements. An example of cooperative game theory is politics, where various groups often form larger coalitions. `{ref} gt:p12`

 * `{bm} non-cooperative game theory` - A branch of game theory where players are either unable to communicate or unable to make binding agreements. An example of non-cooperative game theory is competing firms that are hampered from colluding due to anti-trust laws.  `{ref} gt:p12`

 * `{bm} ordinal payoff/(ordinal payoff|ordinal pay-off)/i` - A game where the preferences of discrete outcomes are ranked using numbers. For example, the preference for the type of cake to consume at a birthday party may be ...

   0. no cake available
   1. non-chocolate cake
   2. chocolate cake

   Item 2 (chocolate cake) is preferable over item 1 (non-chocolate cake), which is preferable over 0 (no cake).  `{ref} gt:p12`

 * `{bm} cardinal payoff` - A game where the preference of outcome is based on quantities (e.g. amount of money) rather than a ranking of discrete items based on preference (ordinal payoffs).  `{ref} gt:p12`

 * `{bm} selfish and greedy` - A player that focuses exclusively on itself when evaluating outcomes (selfish) and has preference for an outcome where it gains more over less (greedy). `{ref} gt:p18`

 * `{bm} fair-minded` - A player whose preference is that all players benefit equally. `{ref} gt:p18`

 * `{bm} benevolent/(benevolent|benevolence)/i` - A player that, when comparing a set of possible outcomes where they gain nothing, has a preference for other players gaining more over less. `{ref} gt:p18`

 * `{bm} preference` - Given a set of outcomes, a player's preferences are the order in which those outcomes are desired. It's not safe to assume that all players in a game are selfish and greedy. For example, a player may benevolent and fair-minded. `{ref} gt:p18`

 * `{bm} strategy/(strategy|strategies)/i` - One of many choices that a player has in a game. `{ref} gt:p19`

 * `{bm} game-frame/(game-frame|game frame)/i` - The cartesian product of each player's strategies in a game, where each output has a set of outcomes. `{ref} gt:p18-19` For example, the game-frame below is for a scenario where Alice's strategies are `{Lie, Get Violent, Stay Silent}` and Bob's strategies are `{Truth, Lie}`.
  
   ```
   (Lie, Truth)         -> A freed, B jailed
   (Lie, Lie)           -> A freed, B freed
   (Get Violent, Truth) -> A jailed, B jailed
   (Get Violent, Lie)   -> A jailed, B freed
   (Stay Silent, Truth) -> A freed, B jailed
   (Stay Silent, Lie)   -> A freed, B freed
   ``` 

   If there are only two players, a game-frame can be represented as a table. `{ref} gt:p19`

   |             |        Truth       |     Lie           |
   |-------------|--------------------|-------------------|
   | Lie         | A freed, B jailed  | A freed, B freed  |
   | Get Violent | A jailed, B jailed | A jailed, B freed |
   | Stay Silent | A freed, B jailed  | A freed, B freed  |

 * `{bm} strategic form` - Representation of a game frame as a tuple with 4 items, where item ...

   1. is a set of players: `I = {1, 2, ..., n}`
   2. is the strategies for each player, represented as a list of sets: `(S1, S2, ..., Sn)`. The cartesian product of these sets is denoted as just `S`, where each element of the set is called a strategy profile.
   3. is the set of outcomes: `O`.
   4. is a function that associates each strategy profile in `S` with an outcome in `O`: `f : S -> O` where `f(s) E O`.

   `{ref} gt:p19`

   TODO: WRITE CODE AND CONTINUE

   TODO: WRITE CODE AND CONTINUE

   TODO: WRITE CODE AND CONTINUE

   TODO: WRITE CODE AND CONTINUE

   TODO: WRITE CODE AND CONTINUE

   TODO: WRITE CODE AND CONTINUE

   TODO: WRITE CODE AND CONTINUE

   TODO: WRITE CODE AND CONTINUE

   TODO: WRITE CODE AND CONTINUE