<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Don't `std::move` into a variable and pass that variable to the constructor. The reason is that the variable will be treated as an lvalue (an lvalue to an rvalue reference), meaning that the copy constructor will get invoked instead of the move constructor.
</div>

