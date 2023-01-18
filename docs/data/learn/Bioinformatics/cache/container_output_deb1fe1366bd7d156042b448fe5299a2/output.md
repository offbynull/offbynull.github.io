<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

In an HMM, there can't be a cycle of non-emitting hidden states. If there is, the Viterbi graph will explode out infinitely. For example, if C and D pointed to each other in the HMM diagram above, its Viterbi graph would continue exploding out forever.
</div>

