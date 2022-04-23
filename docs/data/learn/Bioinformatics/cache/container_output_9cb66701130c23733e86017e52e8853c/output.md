<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

A further somewhat related optimization: Rather than making copies of the string to assign to edges, make string views that reference the original sequences. Python apparently doesn't have a string view class and when you slice a string it copies internally, making it inefficient.
</div>

