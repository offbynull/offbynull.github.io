<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Notice that the operators are more or less array / pointer behaviour. Given something like `int *` pointing to the beginning of an array, ...

 * incrementing it by 1 (`++`) moves it to the next element of the array via pointer arithmetic.
 * dereferencing it (`*`) provides the value at the array element its points to.
 * testing it using inequality (`!=`) is a way to check if it hasn't gone past the last array element.

An iterator is basically a set of operators that walk elements in the same way as you would an array. A class can implement the operator overloads and behave the same way.
</div>

