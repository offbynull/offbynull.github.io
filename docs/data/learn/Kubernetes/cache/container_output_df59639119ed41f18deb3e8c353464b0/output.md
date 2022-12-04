<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

CPU resources can also be dynamically updated without restarting the pod / container process. The environment variable for this likely won't update either, but it isn't restricted like labels / annotations are. There may be other reasons that labels / annotations aren't allowed. Maybe Linux has a cap on how large a environment variable can be, and there's a realistic possibility that labels / annotations can exceed that limit?
</div>

