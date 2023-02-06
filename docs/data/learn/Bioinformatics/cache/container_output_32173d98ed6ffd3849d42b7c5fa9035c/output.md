<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The example is for B→A after index 1 of the [y, y, z, z], ...

```{svgbob}
                                    "EXPLODED OUT HMM"

               y                  y                  z                  z            
                                                                                     
            +----+                                +----+             +----+          
            | A0 |                                | A2 +------------>| A3 +---.      
       .--->|    +.                        .----->|    +.            |    |   |      
       |    +----+ \                      /       +----+ \           +----+   v      
+------+-+          \                    /                \                  +------+
| SOURCE |           \                  /                  \                 | SINK |
+------+-+            \                /                    \                +------+
       |    +----+     \       +----+ /                      \       +----+   ^ ^    
       '--->| B0 |      '----->| B1 +'                        '----->| B3 |   | |    
            |    |     .------>|    |                                |    +---' |    
            +-+--+    /        +----+                                +-+--+     |    
              |      /                                                 |        |    
              v     /                                                  v        |    
            +----+ /                                                 +----+     |    
            | C0 +'                                                  | C3 +-----'    
            +----+                                                   +----+          
```

But a more illustrative example would be for A→B after index 1 of the [y, y, z, z], ...

```{svgbob}
            +----+             +----+                                +----+          
            | A0 +------------>| A1 |                                | A3 +---.      
       .--->|    |             |    +.                        .----->|    |   |      
       |    +----+             +----+ \                      /       +----+   v      
+------+-+                             \                    /                +------+
| SOURCE |                              \                  /                 | SINK |
+------+-+                               \                /                  +------+
       |    +----+                        \       +----+ /           +----+   ^ ^    
       '--->| B0 |                         '----->| B2 +'            | B3 |   | |    
            |    |                                |    |     .------>|    +---' |    
            +-+--+                                +-+--+    /        +-+--+     |    
              |                                     |      /           |        |    
              v                                     v     /            v        |    
            +----+                                +----+ /           +----+     |    
            | C0 |                                | C2 +'            | C3 +-----'    
            +----+                                +----+             +----+          
```

In the above diagram, SOURCE→B0→C0 is a dead-end. The graph algorithm removes such dead-ends before computing the graph. That means, when you filter to a specific edge from an emission index, that filtering process will remove any dead-ends caused by the filtering as well.

```{svgbob}
            +----+             +----+                                +----+          
            | A0 +------------>| A1 |                                | A3 +---.      
       .--->|    |             |    +.                        .----->|    |   |      
       |    +----+             +----+ \                      /       +----+   v      
+------+-+                             \                    /                +------+
| SOURCE |                              \                  /                 | SINK |
+--------+                               \                /                  +------+
                                          \       +----+ /           +----+   ^ ^    
                                           '----->| B2 +'            | B3 |   | |    
                                                  |    |     .------>|    +---' |    
                                                  +-+--+    /        +-+--+     |    
                                                    |      /           |        |    
                                                    v     /            v        |    
                                                  +----+ /           +----+     |    
                                                  | C2 +'            | C3 +-----'    
                                                  +----+             +----+          
```
</div>

