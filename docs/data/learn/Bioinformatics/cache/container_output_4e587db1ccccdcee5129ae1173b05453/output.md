<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If you're trying to determine if the the components of the gene expression vectors follow the same pattern regardless of scale OR offset, this is the similarity to use. They may have similar patterns even though they're scaled differently or offset differently. For example, both genes below may be influenced by the same transcription factor, but their base expression rates are different so the transcription factor influences their gene expression proportionally.

```{svgbob}
"gene A's expression"          "gene B's expression"
"across time-points"           "across time-points"
                               
   10|     *       *                                    
 v  8|    / \     /             v  9|         
 a  6|   /   \   /              a  7|   *   * 
 l  4|  /     \ /               l  5|  / \ / 
 u  2| *       *                u  3| *   *  
 e  0|                          e  1| 
     +--------------                +---------
       0   1   2   3                  0 1 2 3 
          index                        index  
```
</div>

