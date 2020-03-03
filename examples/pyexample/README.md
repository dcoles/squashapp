# Python Example

A simple Python app (a HTTP GET client using [requests](http://python-requests.org/)).

It can be built and run as follows:

```bash
tools/prepare_python examples/pyexample/usr/src/pyexample examples/pyexample
./build_squashapp --embed examples/pyexample usr/bin/pyexample
./pyexample.run https://httpbin.org/get
```

This example uses a [`.env` file](.env) to set the `PYTHONPATH` environment
variable so that Python can find the packages included in the SquashApp.
