<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Similar to a Java `HashMap`, a `std::unordered_set` has concept_NORMs such as bucket count and load factor. It'll automatically add more buckets and rehash once the load factor reaches some point, all of which is tunable if you deem the performance of the defaults as not good. Alternatively, you can always trigger a rehash manually.

Those features aren't discussed here.
</div>

