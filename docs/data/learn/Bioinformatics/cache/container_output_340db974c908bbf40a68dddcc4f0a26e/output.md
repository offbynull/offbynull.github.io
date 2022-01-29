<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What do you do on division by 0? Division by 0 means that the point pairings boil down to a  single point. There is no single line that "fits" through just 1 point (there are an infinite number of lines).

```{svgbob}
"* r is the proximity quantity described above."

"vector A = (5, 5, 5, 5)"
"vector B = (7, 7, 7, 7)"
                                           
                                           
  15|                                        
    |                                        
  13|                                        
    |                                        
  11|                                        
    |                                        
   9|                                        
B   |                                        
   7|           ●
    |  
   5|  
    |                                        
   3|                                        
    |                                        
   1|                                        
    |                                        
    +----------------------------------      
        1   3   5   7   9   11  13  15       
                      A
```

So what's the correct action to take in this situation? Assuming that both vectors consist of a single value repeating n times (can there be any other cases where this happens?), then maybe what you should do is set it as maximally correlated (1.0)? If you think about it in terms of the "pattern matching" component plots discussion, each vector's "component plot is a straight line.

```{svgbob}
"plot of (5,5,5,5)'s"     "plot of (7,7,7,7)'s"   
"components by index"     "components by index"
                                               
                                               
 v  9|                    v  9|              
 a  7|                    a  7| *-*-*-*             
 l  5| *-*-*-*            l  5| 
 u  3|                    u  3|               
 e  1|                    e  1|               
     +---------               +---------      
       0 1 2 3                  0 1 2 3       
        index                    index        
```

It could just as well be interpreted as having no correlation (-1.0) because a mirror of a straight line (across the x-axis, as discussed above) is just the same straight line?

I don't know what the correct thing to do here is. My instinct is to mark it as maximum correlation (1.0) but I'm almost certain that that'd be wrong. The Internet isn't providing many answers -- they all say its either undefined or context dependent.
</div>

