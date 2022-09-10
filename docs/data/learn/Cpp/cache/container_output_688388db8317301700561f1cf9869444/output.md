<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

You may be wondering what the point of partitioning is if you can only partition into two groups. You can partition into more than two groups by iteratively calling `std::partition()`. For example, imagine you need to partition into 4 groups: Call `std::partition()` with the predicate that partitions by the first group's criteria, which will end up partitioning and returning an iterator that points to the element just after where all the elements for the first group got moved to. Then call `std::partition()` with the second group's criteria but use the return value of the previous `std::partition()` for the starting iterator. Do the same thing for the third and fourth group.
</div>

