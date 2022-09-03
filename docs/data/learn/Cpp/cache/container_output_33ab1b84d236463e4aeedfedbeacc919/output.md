<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If you don't supply a base, it defaults the base to `std::current_path()`.

According to [cppreference](https://en.cppreference.com/w/cpp/filesystem/relative), this also resolves symbolic links, meaning the path you submit has to exist? The text seems unclear. There's also `std::filesystem::proximate()` which seems to be more loose with the rules? I'm not exactly sure what's going on here. The documentation isn't clear.
</div>

