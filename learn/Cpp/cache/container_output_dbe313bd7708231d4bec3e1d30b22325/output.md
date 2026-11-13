<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It's possible to remove the `class` from `enum class`, which heavily loosens type-safety and scope. By removing `class`, the options within have their values implicitly converted to integers and you don't need the resolution scope operator (their options are accessible at the same level as an enum).

```c++
enum MyEnum { // no class keyword
   OptionA,
   OptionB,
   OptionC
};

MyEnum x {OptionC}; // this is okay -- don't have to use MyEnum::OptionC
int y {OptionC};    // this is okay -- options are integers
```

You should prefer `enum class`.
</div>

