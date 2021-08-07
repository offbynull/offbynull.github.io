<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Confused about the second point? Think of it like this, species m splits into species a and b. That split happened at the same time, meaning a and b always have the same age difference when compared against their parent m (e.g. m is always 30 years older)...

```{svgbob}
    (age=30) m      
            / \     
        30 /   \ 30
          /     \   
         /       \  
(age=0) a         b (age=0)
```

Likewise, think of what happens if m and its sibling n had split off from g. Unlike m, its sibling n never split, meaning that a, b, and n (all leaf nodes) all have the same age difference when compared against their shared ancestor g (e.g. g is always 70 years older)...

```{svgbob}
                   g (age=70)
                  / \
                 /   \
             40 /     \
               /       \
              /         \ 70
    (age=30) m           \
            / \           \
        30 /   \ 30        \
          /     \           \
         /       \           \
(age=0) a         b (age=0)   n (age=0)
```

In other words, you can think of "age" more so as an "age offset" from leaf nodes rather than the age of the species.
</div>

