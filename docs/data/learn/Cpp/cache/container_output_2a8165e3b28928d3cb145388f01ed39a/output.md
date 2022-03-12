<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

I don't fully understand what the copy constructor and the operator overloads are for. The copy constructor seems to be for cases where you pass in an allocator to some container class (e.g. `vector`) but that container class needs to allocate more than just the type you're interested in. For example, the allocator may be for creating `int`s (e.g. template parameter `T` = `int`) but the container class you're storing those `int`s may have bookkeeping structures that it wraps each `int` in (e.g. each `int` is wrapped as a `Node` object which also contains some extra pointers). This copy constructor "repurposes" the allocator, allowing you to to pass in `MyAllocator<int>` but have it repurposed to `MyAllocator<SomeOtherTypeHere>`.

But if you're copying the guts of one allocator into another but both keep on allocating and deallocating, won't they trip up over each other?

I haven't been able to find answers online as to what's going on here. The book just seems to hand wave it away.
</div>

