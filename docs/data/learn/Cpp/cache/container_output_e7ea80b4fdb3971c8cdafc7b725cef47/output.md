<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book says that sometimes you want to avoid `std::make_shared` because you might need the control block even if the dynamic object goes away (mentions weak pointers). This isn't possible if the control block and the dynamic object are allocated as one, because if they're allocated as one then you can't individually delete them (you can only delete both things at once).
</div>

