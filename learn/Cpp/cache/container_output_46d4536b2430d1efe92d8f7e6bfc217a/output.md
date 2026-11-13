<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Be careful with data members that are invokable (e.g. a member variable that's of type `std::function`). It will not get invoked, and will sometimes it leads to stuff being silently ignored. See [here](https://devblogs.microsoft.com/oldnewthing/20220401-00/?p=106426).

[Here](https://youtu.be/zt7ThwVfap0?t=655)'s a good blurb going over why `std::invoke()` exists.
</div>

