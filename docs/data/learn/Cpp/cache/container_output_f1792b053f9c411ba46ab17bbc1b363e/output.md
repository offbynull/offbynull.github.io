<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

My understanding is that arrays are typically passed to functions as pointers + array length. This is because the array length information is only available at compile-time, meaning that if you have a function that takes in an array, how would it know the size of the array it's working with (it isn't the one who declared it). It looks like you can for the function to an array type of fixed size, but apparently that doesn't mean anything? The compiler doesn't enforce that a caller use an array of that fixed size, and using sizeof on the array will produce a warning saying that it's decaying into a pointer.

```c++
size_t test(int x[10]) {
   return sizeof(x); // compiler warning that this is returning sizeof(int *)
}

int main() {
   int x[3] = { 1, 2, 3 };
   size_t y { test(x) }; // compiler doesn't complain that test() expects int[10] but this is int[3]
   cout << y;
   return 0;
}
```
</div>

