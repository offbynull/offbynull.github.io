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

 * `{bm} homo rationalis` - An agent that acts purposefully and logically to get as close as possible to a set of well-defined goals. `{ref} gt:p12`
 
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

 * `{bm} preference` - Given a set of outcomes, a player's preferences are the order in which those outcomes are desired. It's not safe to assume that all players in a game are selfish and greedy. For example, a player may benevolent or fair-minded. `{ref} gt:p18`

   There are four common ways of representing preferences. Imagine a scenario where, given the outcomes `{o1, o2, o3, o4}`, the preference for those outcomes is `o3` is better than `o1`, which is just as good as `o4`, which in turn is better than `o2` (best is `o3`, worst is `o2`).

    * Relational notation - Represent which outcome has preference over the other using ...
    
      * `>`: `A > B` means outcome A is better than outcome B.
      * `==`: `A == B` means outcome A is just as good as outcome B.

      These preferences are typically written chained together (e.g. `A > B == C` is equivalent to `A > B and B == C`). `{ref} gt:p20`

      The scenario above would be represented as `o3 > o1 == o4 > o2`.

      ```{note}
      The book also provides the following notation: `>=`, where `A >= B` means outcome `A` is at least as good as outcome `B`. Then it goes through a convoluted section that explains `>` and `==` can be represented just by `>=`. For example, given two outcomes `{A, B}`, the relation ...

      * `A == B` can be represented using just `>=` as `A >= B and B >= A`.
      * `A > B` can be represented using just `>=` as `A >= B and not(B >= A)`.

      The problem is, I don't know what "at least as good as" means in terms of the desire for an outcome. If something A is "at least as good as" B (e.g. `A >= B`), there's the possibility that I'll gain more from A vs B, so why wouldn't I always prefer A over B?
      ```

    * Cartesian product - Given the cartesian product of the outcomes with itself, keep only the ordered pairs `(A, B)` where `A` is at least desired as much as `B`. `{ref} gt:p20`

      The scenario above would be represented as follows.
      
      ```python
      {
        (o1, o1), (o1, o4), (o1, o2),
        (o2, o2),
        (o3, o3), (o3, o1), (o3, o4), (o3, o2),
        (o4, o4), (o4, o1), (o4, o2)
      }
      ```

    * Ranked list - Represent which outcome has preference as a list from best-to-worst, where equally desired outcomes are put into the same index.  `{ref} gt:p21`

      The scenario above would be represented as follows.
      
      1. o3
      2. o1 and o4
      3. o2

    * Number assignment - Represent which output has preference by assigning a number to each outcome, where larger numbers are desired more than smaller numbers. `{ref} gt:p21`

      The scenario above could be represented as the following mapping `{o3=30, o1=19, o4=19, o2=6}`.

      ```{note}
      Assigning numbers in this way is sometimes referred to as a utility function. `{ref} gt:p21`
      ```

 * `{bm} utility function/(utility function|utility)/i` - Given a set of outcomes and preferences for those outcomes, a utility function assigns a number to each outcome, where that number identifies that outcome's ranking in terms of preference. Given two outcomes A and B, if ...

   * A is more desired than B (`A>B`), A is assigned a higher number than B. 
   * A is equally desired as B (`A==B`), A is assigned the same number as B.

    `{ref} gt:p21`

   The numbers are simply identifying ranking based on best-to-worst, they aren't quantities. `{ref} gt:p21` As such, there are an infinity number of utility functions that represent the same preference. `{ref} gt:p22` For example, `o3 > o1 == o4 > o2` may be mapped by a utility function as `{o3=30, o1=19, o4=19, o2=6}`, `{o3=3, o1=2, o4=2, o2=-50}`, `{o3=70, o1=3, o4=3, o2=1}`, etc..

   ```{note}
   If the outcomes are drink Coke vs drink Sprite and the utility function assigns `{Coke=30, Sprite=10}, that doesn't mean Coke is 3 times more as desired as Sprite. It simply means Coke is preferred over Sprite.
   ```

 * `{bm} strategy/(strategy|strategies)/i` - One of many choices that a player has in a game. `{ref} gt:p19`

 * `{bm} game frame/(game[-\s]frame)/i` - The cartesian product of each player's strategies in a game, where each output has a set of outcomes. `{ref} gt:p18-19` For example, the game-frame below is for a scenario where Alice's strategies are `{Lie, Get Violent, Stay Silent}` and Bob's strategies are `{Truth, Lie}`.
  
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

 * `{bm} game frame in strategic form/(game[-\s]frame in strategic form)/i` - Representation of a game frame as a tuple with 4 items, where item ...

   1. is a set of players: `I = {1, 2, ..., n}`
   2. is the strategies for each player, represented as a list of sets: `(S1, S2, ..., Sn)`. The cartesian product of these sets is denoted as just `S`, where each element of the set is called a strategy profile.
   3. is the set of outcomes: `O`.
   4. is a function that associates each strategy profile in `S` with an outcome in `O`: `f : S -> O` where `f(s) E O`.

   `{ref} gt:p19`

 * `{bm} game` - A game frame along with the preferences of each player in that game frame. `{ref} gt:p19`

   For example, given players A and B with the following game frame, ...

   |                |      B: Truth       |       B: Lie       |
   |----------------|---------------------|--------------------|
   | A: Lie         | A freed / B jailed  | A freed / B freed  |
   | A: Get Violent | A jailed / B jailed | A jailed / B freed |
   | A: Stay Silent | A freed / B jailed  | A freed / B freed  |

   The preference of player...

   * A is ranked `[A freed / B jailed, A freed / B freed, A jailed / B jailed, A jailed / B freed]`.
   * B is ranked `[A freed / B freed, A jailed / B freed, A jailed / B jailed, A freed / B jailed]`.






TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

TODO: CONTINUE FROM PAGE22 "Utility functions are a particularly convenient way of representing preferences. In fact, by using utility functions one can ..."

