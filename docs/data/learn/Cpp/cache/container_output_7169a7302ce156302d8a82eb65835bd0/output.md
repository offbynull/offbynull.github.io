<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

`auto` is a placeholder for a template parameter, and as such type deduction rules come into play. If you aren't careful, you'll end up with strange or incorrect behaviour. For example, in certain cases the compiler may decide to create a local copy for an argument that gets passed in where you may be expecting a reference.
</div>

