<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Last I recall using this, each compiler required a special flag to turn on modules. Just because your code uses modules doesn't mean the internal C++ libraries (e.g. standard template library, `cstdint`, etc..) are going to expose things as modules. You still have to include those using the `#include <...>` directives (maybe -- I think I remember there being some roundabout way of getting modules to work).
</div>

