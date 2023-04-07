<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This is how I'm thinking about what this formula is doing: When you perform P(X)+P(Y) you're stacking the probabilities together such that it becomes the probability of either G outcome, R outcome, twice the B outcomes. It's 2\*B because B appears in both X and Y.

The reason you're subtracting by the joint probability is because the joint probability includes the set of outcomes that are in both events (X∩Y={B}). !!Meaning!!, when you subtract by P(X∩Y), you're removing 1 of the B's from stacked probability probability.

It might be easier to think of this as outcomes: [B,G]+[B,R]-[B] = [B,B,G,R]-[B] = [B,G,R]
</div>

