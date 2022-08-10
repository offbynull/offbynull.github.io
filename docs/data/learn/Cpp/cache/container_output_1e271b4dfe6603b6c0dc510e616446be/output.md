<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There are a handful of other iterator type traits that build on-top of each other to form a taxonomy of concept_TEMPLATEs for iterators. For example, at the bottom is ...

 * `std::incrementable` / `std::weakly_incrementable` - enforces `it++` and `++it` type traits.
 * `std::input_or_output_iterator` - enforces `*it` type traits and enforces `std::weakly_incrementable`.
 * etc..

I don't think these are useful enough to document.
</div>

