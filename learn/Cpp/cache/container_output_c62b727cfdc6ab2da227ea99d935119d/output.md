<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Look at the template parameters in the example above. It's important that you add `[]` into the template parameter when you're dealing with arrays so the destroy dynamic array operator (`delete[]`) gets used. If the destroy dynamic object operator (`delete`) is used for an array, it's undefined behaviour. Likewise, don't add `[]` into the template parameter if you aren't dealing with arrays.
</div>

