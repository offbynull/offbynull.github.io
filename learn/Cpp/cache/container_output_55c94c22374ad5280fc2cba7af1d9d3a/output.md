<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book mentions that the `std::endian` system covers all possible edge cases, such as the case where some type are big-endian but others are little-endian (tested for in the example above). The other edge case it mentions is where all types are exactly 1 byte in size, in which case the platform has no endian-ness (`std::endian::little == std::endian::native == std::endian::big`).
</div>

