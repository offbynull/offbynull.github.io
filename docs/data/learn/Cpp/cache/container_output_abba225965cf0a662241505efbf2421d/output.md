<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It seems like there's some implicit conversions to boolean that are possible with pointers. If whatever the pointer is going to expects a boolean, its implicitly converted to `ptr != nullptr`? So in if / while/ for conditions, you can just use the pointer as is without explicitly writing out a condition?
</div>

