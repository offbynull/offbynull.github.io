<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

See [here](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html) for a list of base images with language runtimes that have "runtime interface client" support already builtin.

See [here](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html) for specs on how the "runtime interface client" should be implemented. It sounds like this is a client that queries a server? So the container starts and the first thing it does it pulls a domain from the environment variables and queries a web service at that domain for the payload to run? They have pre-built clients up on GitHub for each language runtime.
</div>

