<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book says that a static extent span's size can't be 0 and if it is you'll get a compile-time error. When I try this in G++12, I don't get an error and `size()` appropriately reports 0. Also, the documentation [here](https://en.cppreference.com/w/cpp/container/span) says nothing about this.
</div>

