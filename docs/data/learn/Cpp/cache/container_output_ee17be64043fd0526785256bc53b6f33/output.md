<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Make sure to turn off the C++ extension's intellisense support or else it'll interfere with clangd's superior intellisense support. You can do this by adding the following to your `.vscode/settings.json file`...

```json
{
    "C_Cpp.intelliSenseEngine": "Disabled",
    "C_Cpp.autocomplete": "Disabled",  // So you don't get autocomplete from both extensions.
    "C_Cpp.errorSquiggles": "Disabled", // So you don't get error squiggles from both extensions (clangd's seem to be more reliable anyway).
}
```
</div>

