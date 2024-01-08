<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Lambda puts limits on how big the zip / container can be. If using a ...

* zip, as of today the limits are that the zip must be < 50mb compressed and < 250mb uncompressed.
* container image, as of today the limits are that the image must be < 10gb.

If using a zip, one common pattern is to include dependencies within the zip via `pip install -r requirements.txt -t .` which install the packages into the current directory rather than the Python installation. Another common examples is to use "Lambda layers", which is another zip file that can be shared across various function zips and contains supplementary data like dependencies

 If you have dependencies or custom runtimes, using containers may be a better idea.
</div>

