<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Which should you use? I'm not sure the difference. `std::chrono::sys_days` is shorthand for `std::chrono::time_point<std::chrono::system_clock, std::chrono::days>`, which is the time point type for the system clock. `std::chrono::local_days` expands to the same thing but for the local clock. I'm not sure what local clock actually is. It wasn't listed as one of the clocks.
</div>

