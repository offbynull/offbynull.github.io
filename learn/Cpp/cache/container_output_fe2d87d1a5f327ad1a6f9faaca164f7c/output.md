<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

According to [cppreference](https://en.cppreference.com/w/cpp/filesystem/canonical), this also resolves symbolic links, meaning the path you submit has to exist? The text seems unclear. There's also `std::filesystem::weakly_canonical()` which will only "resolve" up until the last known path element and just append the rest? I don't know for sure.
</div>

