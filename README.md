# SquashApp

A self-extracting SquashFS application builder.

## Requirements

- [`bash`](https://www.gnu.org/software/bash) (or compatible [`mksh`, `busybox`, ...])
- [`mksquashfs`](https://github.com/plougher/squashfs-tools)
- [`squashfuse`](https://github.com/vasi/squashfuse)


## Building a SquashApp

```bash
Usage: ./build_squashapp [--embed] [-h|--help] <sourcedir> [<main>]
Options and arguments:
    --embed        embed runtime into SquashApp
    -h, --help     show help (this text)

    <sourcedir>    directory to build SquashApp from
    <main>         relative path of main executable (default: `basename <sourcedir>`)
```

For example:

```bash
build_squashapp examples/helloworld/ bin/helloworld
```

This will produce a SquashApp named `helloworld.run`.


# Running a SquashApp

Just run it like any ordinary executable!

```bash
./helloworld.run "${USER}"
```


# License

Licensed under the [MIT License](/LICENSE).
