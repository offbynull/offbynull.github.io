<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Make sure that you don't have other C++ extensions installed. I'd initially installed a Makefile plugin into vscode that was tripping up the CMake plugin and breaking my intellisense.

You can swap out "C++ Extension" in the C++ extension pack for the clangd extension. It'll work with the CMake plugin and provide intellisense / auto-complete / formatting / etc.. support using LLVM Clang's engine.
</div>

