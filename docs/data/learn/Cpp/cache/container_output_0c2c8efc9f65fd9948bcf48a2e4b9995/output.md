<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There is no template parameter for the allocator. You just pass it in as the first constructor argument and it should just work.

There is no custom deleter with `std::allocate_shared` because the deletion happens via the allocator. Both the control block and the dynamic object are being allocated and deallocated together.
</div>

