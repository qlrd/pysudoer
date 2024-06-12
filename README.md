# pysudoer

[![codecov](https://codecov.io/gh/qlrd/pysudoer/graph/badge.svg?token=WFJJQNVA4M)](https://codecov.io/gh/qlrd/pysudoer)

This is a [@o/elecron-sudo](https://www.npmjs.com/package/@o/electron-sudo)'s python port.

Run a subprocess with administrative privileges,
prompting the user with a graphical OS dialog if necessary.

- `Windows`, uses [elevate utility](https://github.com/automation-stack/electron-sudo/tree/master/src/vendor/win32) with native `User Account Control (UAC)` prompt (no `PowerShell` required)

- `OS X`, uses bundled [applet](https://github.com/automation-stack/electron-sudo/tree/master/src/bin/applet.app) (inspired by  [Joran Dirk Greef](https://github.com/jorangreef))

- `Linux`, uses system `pkexec` or [gksudo](http://www.nongnu.org/gksu) (system or bundled).


If you don't trust binaries bundled in `pip` package you can manually build tools and use them instead.

## Installing


Clone the project:

```bash
git clone https://github.com/qlrd/pysudoer.git
```

### Setup

Install poetry:

```bash
pipx install poetry
```

Enter in `pysudoer` folder:

```bash
cd pysudoer
```

Install dependencies:

```bash
poetry install
```

### Pre-commit

Before commit some changes, we recommend to follow a three step:

* Text formatting: 

```bash
poetry run poe format
```

* Code linting:

```bash
poetry run poe lint
```

* Test:

```bash
poetry run poe test
```

### Build

To build `.tar.gz` and `.whl` files:

```bash
poetry build
```

