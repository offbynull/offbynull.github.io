<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

WARNING: The book is saying that there is no hard requirement for a container to return copies vs references. Most of the time a container returns references, but in special cases it may return a copy of some object. For example, `vector<bool>` has a template specialization that returns a proxy object rather than a direct reference (`std::vector<bool>::reference`).
</div>

