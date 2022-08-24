<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Why didn't the 3rd failed example above work? Maybe what needs to happens is that you need to parse it as `std::chrono::year_month` (as is done in the 4th example), then finagle it into a duration. Maybe something like what's below.

```c++
std::chrono::year_month d1 { 2021y, August };
std::chrono::year_month d2 { d1 - std::chrono::months(1) };
auto dur { d1 - d2 };  // 1[2629746]s  -- this is the num of seconds in August? nope. it comes out to 30.5 days while aug has 31 days
```
</div>

