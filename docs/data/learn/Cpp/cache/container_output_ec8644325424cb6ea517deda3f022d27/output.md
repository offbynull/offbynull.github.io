<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Also, as of C++20, there is no built-in character set encoding/decoding functionality, so how exactly is it converting character set encodings (e.g. utf-8 characters to whatever the platform is expecting for its filesystem)? `char` is for the platform's encoding - so maybe just use that and ignore everything else?
</div>

