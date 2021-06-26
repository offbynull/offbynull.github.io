<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The example above tests against a tree that's both a rooted tree and a non-simple tree (Feline to Bear is a non-branching path with > 0 nodes in between). The tree doesn't have to be rooted or non-simple. In fact, I suspect the book is implying that it should be both un-rooted and simple. I'm guessing that if you limit your search scope to simple trees and find nothing, there won't be any non-simple trees either: Non-simple trees are essentially the same as simple trees but with extra nodes spliced between non-branching paths.

The example above as a simple tree:


```{svgbob}
            z
       *--------* Bear 
      / \
  w  /   \ x
    /     \
   *       *
  Cat     Lion
```

This simple tree version gets solved to `w = 2`, `x = 1`, and `z = 2`.
</div>

