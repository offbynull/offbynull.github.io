<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The example above doesn't include non-emitting hidden states. A non-emitting hidden state means that a transition to that hidden state doesn't result in a symbol emission. In other words, the emission index wouldn't increment, meaning the exploded HMM node would end up under the same column as the node that's pointing to it.

Consider if fouler bat in the example above had a transition to a non-emitting hidden state called bingo. At ...

 * fouler bat0, the transition to bingo would be fouler bat0 → bingo0.
 * fouler bat1, the transition to bingo would be fouler bat1 → bingo1.
 * etc...

Exploded bingo nodes maintain the same index as their exploded fouler bat predecessor because bingo is a non-emitting hidden state (nothing gets emitted when you transition to it, meaning you stay at the same index).
</div>

