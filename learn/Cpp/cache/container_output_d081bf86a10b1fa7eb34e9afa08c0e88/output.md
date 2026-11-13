<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What type is `sys_tp_rounded`? It's `std::chrono::sys_days`, which is shorthand for `std::chrono::time_point<std::chrono::system_clock, std::chrono::days>`. The `std::chrono::year_month_day` constructor also accepts `std::chrono::local_days` -- I'm unsure which clock generates that (maybe utc clock?).
</div>

