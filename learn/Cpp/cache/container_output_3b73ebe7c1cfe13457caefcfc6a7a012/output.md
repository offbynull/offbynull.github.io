<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The exact rules here seem hard to definitively pin down. If you have two overloads of a function, one accepting int16 and int64, it'll fail when you try to call it with int8 claiming that it's too ambiguous. The best thing to do is to just ask the compiler to either warn on implicit conversion (`-Wconversion`) flag or on narrowing implicit conversion (`-Wnarrowing` / `-Wno-narrowing`). These flags may not be included under `-Wall`.
</div>

