# kivy-sudoer

This is a [@o/elecron-sudo](https://www.npmjs.com/package/@o/electron-sudo)'s python port.

Run a subprocess with administrative privileges,
prompting the user with a graphical OS dialog if necessary.

- `Windows`, uses [elevate utility](https://github.com/automation-stack/electron-sudo/tree/master/src/vendor/win32) with native `User Account Control (UAC)` prompt (no `PowerShell` required)

- `OS X`, uses bundled [applet](https://github.com/automation-stack/electron-sudo/tree/master/src/bin/applet.app) (inspired by  [Joran Dirk Greef](https://github.com/jorangreef))

- `Linux`, uses system `pkexec` or [gksudo](http://www.nongnu.org/gksu) (system or bundled).


If you don't trust binaries bundled in `pip` package you can manually build tools and use them instead.

