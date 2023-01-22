<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The HMM above has non-emitting hidden states (C).

One thing that the 2nd "recall that" point above doesn't cover is a hidden state transition to a non-emitting hidden state. If the hidden path travels through a non-emitting hidden state, leave out multiplying by the emission probability. For example, if there's a transition from B to C but C is a non-emitting hidden state, the probability should simply be Pr(B→C).

That's why some of the probabilities being multipled above don't list an emission
</div>

