<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

In the HMM above, each emitting hidden state has a 100% symbol emission probability for emitting the symbol at the sequence index that it's for vs a 0% probability of embedding all other symbols. For example, E10 has a ...

 * 100% probability of emitting symbol h.
 * 0% probability of emittin symbol i.

As such, the HMM diagram above embeds the sole symbol emission for each E node directly in that E node vs drawing out dashed edges / nodes to symbol emission. Doing this makes it easier to understand what's going on.
</div>

