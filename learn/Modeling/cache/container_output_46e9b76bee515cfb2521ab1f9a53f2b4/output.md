<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

For dependent events, note that the inputs into the conditional probability can be swapped: P(A∩B) = P(A)\*P(B|A) = P(B)\*P(A|B). For example, consider a jar with 2 As and 4 Bs. The probability of first selecting an A and then a B can be visualized as follows.

```{svgbob}
             "P(A) * P(B|A)"                                     "P(B) * P(A|B)"
             "4/6 * 1/5"                                         "2/6 * 2/5"              
             "4/30 = 2/15"                                       "4/30 = 2/15"            
                                                                                         
  .-     -.                 .-     -.                 .-     -.                 .-     -.  
  |       |  "Remove a A"   |       |                 |       |  "Remove a B"   |       |  
  | A B B | --------------> |   B B |                 | A B B | --------------> | A   B |  
  | B B A |                 | B B A |                 | B B A |                 | B B A |  
  '-------'                 '-------'                 '-------'                 '-------'  
  "2A vs 4B"                "1A vs 4B"                "2A vs 4B"                "2A vs 3B" 
```

Both formulas produce the same result but it feels like the second formula makes it more intuitive to understand. The first operand is the probability of selecting one of the 4 A: P(A). Once that A's been selected and removed from the jar (without replacement), the second operand is the conditional probability of selecting a B.
</div>

