## MyCompat Overview
A lightweight compatibility library designed to facilitate the retrieval of system version information and various other system details.

This library is derived from [`PyInstaller.compat`](https://github.com/pyinstaller/pyinstaller/blob/develop/PyInstaller/compat.py) and incorporates a custom freezing system. This system optimizes the handling of 
different variables by evaluating them only when necessary and caching their values globally, akin to Just-In-Time (JIT) compiling.

### Installation
You can install the library using `pip`.

``` bash
pip install mycompat
```

The module is not supported in Python versions below 3.3.

### Usage
It works just like a normal module, with a stub file to facilitate type hinting.

You can import the entire module or import specific attributes from it, just like with any other module.

``` python
from mycompat import (
    is_win,
    is_darwin,
    is_linux
)

import mycompat

mycompat.is_win
mycompat.is_darwin
mycompat.is_linux
```

Optionally, you can also unfreeze all variables ahead of time using the unfreeze function provided within the module.

``` python
import mycompat

mycompat.unfreeze()
```

## Disclaimer
The freezing feature is experimental and has not been tested in a production environment. 
While it is not dangerous to use, its effectiveness in improving performance has not been proven.