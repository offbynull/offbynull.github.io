<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If you have a `void *` and you want to do raw memory manipulation at that address, use a `std::byte *` instead. Why not just use `char *` instead? Is a `char` guaranteed to be 1 byte (I think it is)? According to [this](https://stackoverflow.com/a/46151026), it's because certain assumptions about `char`s may not hold with bytes? I don't know. Just remember `std::byte *` if you're working with raw data.
</div>

