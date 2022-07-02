<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The above example class is feeding itself as a template parameter to `std::ranges::view_interface`. This is a common C++ idiom referred to as the curiously recurring template pattern (CRTP) which allows for feeding the derived class back into a templated base class. Something to do with compile-time polymorphism.
</div>

