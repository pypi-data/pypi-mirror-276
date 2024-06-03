import sys
import os

# This compatibility module redefines standard import mechanisms in Python. 
# It optimizes the handling of certain boolean variables by 'freezing' them, 
# ensuring they are evaluated only when needed. This optimization minimizes 
# unnecessary function calls for accessing individual variables. Once frozen, 
# a variable retains its computed value globally, eliminating the need for 
# repeated evaluation. It works similarly to Just-In-Time (JIT) compiling.

# For more advanced users, a function is provided to unfreeze all variables 
# that are actively frozen. This can be achieved by calling 'unfreeze'.

# This cache variable helps prevent repeated isinstance checks on
# values that have already been unfrozen.
_cache = {}

class FrozenContext:
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback
    
    def __call__(self):
        value = self.callback()
        _cache[self.name] = value
        globals()[self.name] = value
        return value

class FrozenModule:
    def __getattribute__(self, name):
        try:
            instance = globals()[name]
        except KeyError:
            raise ImportError(f"cannot import name '{name}' from 'mycompat' ({os.path.abspath(__file__)})")
        
        if name in _cache:
            return _cache[name]

        if isinstance(instance, FrozenContext):
            return instance()
        
        return instance

class Freezer:
    @staticmethod
    def register(name, callback):
        globals()[name] = FrozenContext(name, callback)

    @staticmethod
    def unfreeze():
        """
        Unfreezes all variables that are currently frozen.

        This function iterates over all global variables that are instances of `FrozenContext`
        and forces their evaluation, updating their values in the global namespace.
        """

        for name, instance in globals().items():
            if name in _cache:
                continue

            if name.startswith("__") and name.endswith("__"):
                continue

            if isinstance(instance, FrozenContext):
                instance()

# Override the imported 'mycompat' module for custom '__getattribute__' implementation.
sys.modules["mycompat"] = FrozenModule()

# Import the util file in the project directory.
from importlib.machinery import SourceFileLoader

util = SourceFileLoader("util", os.path.join(os.path.dirname(__file__), "util.py")).load_module()

import subprocess
import platform

# The below compatibility variables were taken from PyInstaller's compat file.
# https://github.com/pyinstaller/pyinstaller/blob/develop/PyInstaller/compat.py
Freezer.register("is_64bits", lambda: sys.maxsize > 2**32)

Freezer.register("is_py33",  lambda: sys.version_info >= (3, 3))
Freezer.register("is_py34",  lambda: sys.version_info >= (3, 4))
Freezer.register("is_py35",  lambda: sys.version_info >= (3, 5))
Freezer.register("is_py36",  lambda: sys.version_info >= (3, 6))
Freezer.register("is_py37",  lambda: sys.version_info >= (3, 7))
Freezer.register("is_py38",  lambda: sys.version_info >= (3, 8))
Freezer.register("is_py39",  lambda: sys.version_info >= (3, 9))
Freezer.register("is_py310", lambda: sys.version_info >= (3, 10))
Freezer.register("is_py311", lambda: sys.version_info >= (3, 11))
Freezer.register("is_py312", lambda: sys.version_info >= (3, 12))

is_win = sys.platform.startswith('win')
Freezer.register("is_win_10", lambda: is_win and (platform.win32_ver()[0] == '10'))
Freezer.register("is_win_10", lambda: is_win and (platform.win32_ver()[0] == '11'))
Freezer.register("is_win_wine", util._Callback.is_win_wine)  # Running under Wine.

is_cygwin = sys.platform == 'cygwin'
is_darwin = sys.platform == 'darwin'  # Mac OS X

# Unix platforms
is_linux = sys.platform.startswith('linux')
is_solar = sys.platform.startswith('sun')  # Solaris
is_aix = sys.platform.startswith('aix')
is_freebsd = sys.platform.startswith('freebsd')
is_openbsd = sys.platform.startswith('openbsd')
is_hpux = sys.platform.startswith('hp-ux')

# Some code parts are similar to several unix platforms (e.g. Linux, Solaris, AIX).
# Mac OS is not considered as unix since there are many platform-specific details for Mac.
is_unix = is_linux or is_solar or is_aix or is_freebsd or is_hpux or is_openbsd

# Linux distributions such as Alpine or OpenWRT use musl as their libc implementation and resultantly need specially
# compiled bootloaders. On musl systems, ldd with no arguments prints 'musl' and its version.
Freezer.register("is_musl", lambda: is_linux and "musl" in subprocess.run(["ldd"], capture_output=True, encoding="utf-8").stderr)

# macOS version
Freezer.register("_macos_ver", lambda: tuple(int(x) for x in platform.mac_ver()[0].split('.')) if is_darwin else None)

# macOS 11 (Big Sur): if python is not compiled with Big Sur support, it ends up in compatibility mode by default, which
# is indicated by platform.mac_ver() returning '10.16'. The lack of proper Big Sur support breaks find_library()
# function from ctypes.util module, as starting with Big Sur, shared libraries are not visible on disk anymore. Support
# for the new library search mechanism was added in python 3.9 when compiled with Big Sur support. In such cases,
# platform.mac_ver() reports version as '11.x'. The behavior can be further modified via SYSTEM_VERSION_COMPAT
# environment variable; which allows explicitly enabling or disabling the compatibility mode. However, note that
# disabling the compatibility mode and using python that does not properly support Big Sur still leaves find_library()
# broken (which is a scenario that we ignore at the moment).
# The same logic applies to macOS 12 (Monterey).
Freezer.register("is_macos_11_compat", lambda: bool(_macos_ver) and _macos_ver[0:2] == (10, 16)) # Big Sur or newer in compat mode
Freezer.register("is_macos_11_native", lambda: bool(_macos_ver) and _macos_ver[0:2] >= (11, 0))  # Big Sur or newer in native mode
Freezer.register("is_macos_11", lambda: is_macos_11_compat or is_macos_11_native)

# In a virtual environment created by virtualenv (github.com/pypa/virtualenv) there exists sys.real_prefix with the path
# to the base Python installation from which the virtual environment was created. This is true regardless of the version
# of Python used to execute the virtualenv command.
#
# In a virtual environment created by the venv module available in the Python standard lib, there exists sys.base_prefix
# with the path to the base implementation. This does not exist in a virtual environment created by virtualenv.
#
# The following code creates compat.is_venv and is.virtualenv that are True when running a virtual environment, and also
# compat.base_prefix with the path to the base Python installation.
Freezer.register("base_prefix", lambda: os.path.abspath(getattr(sys, 'real_prefix', getattr(sys, 'base_prefix', sys.prefix))))

# Ensure `base_prefix` is not containing any relative parts.
Freezer.register("is_venv", lambda: base_prefix != os.path.abspath(sys.prefix))
Freezer.register("is_virtualenv", lambda: is_venv)

# Conda environments sometimes have different paths or apply patches to packages that can affect how a hook or package
# should access resources. Method for determining conda taken from https://stackoverflow.com/questions/47610844#47610844
Freezer.register("is_conda", lambda: os.path.isdir(os.path.join(base_prefix, 'conda-meta')))

# Similar to ``is_conda`` but is ``False`` using another ``venv``-like manager on top.
Freezer.register("is_pure_conda", lambda: os.path.isdir(os.path.join(sys.prefix, 'conda-meta')))

# Full path to python interpreter.
python_executable = getattr(sys, '_base_executable', sys.executable)

# Is this Python from Microsoft App Store (Windows only)? Python from Microsoft App Store has executable pointing at
# empty shims.
Freezer.register("is_ms_app_store", lambda: is_win and os.path.getsize(python_executable) == 0)

# Gets the system machine type.
machine = platform.machine()

# macOS's platform.architecture() can be buggy, so we do this manually here. Based off the python documentation:
# https://docs.python.org/3/library/platform.html#platform.architecture
if is_darwin:
    Freezer.register("architecture", lambda: '64bit' if sys.maxsize > 2**32 else '32bit')
else:
    Freezer.register("architecture", lambda: platform.architecture()[0])

# Machine suffix for bootloader.
if is_win:
    # On Windows ARM64 using an x64 Python environment, platform.machine() returns ARM64 but
    # we really want the bootloader that matches the Python environment instead of the OS.
    Freezer.register("simple_machine", lambda: util._pyi_machine(os.environ.get("PROCESSOR_ARCHITECTURE", platform.machine()), platform.system()))
else:
    Freezer.register("simple_machine", lambda: util._pyi_machine(platform.machine(), platform.system()))

# Detects if a python script has been packaged into an executable.
Freezer.register("is_frozen", lambda: getattr(sys, "frozen", False))

# Register 'unfreeze' function in the global namespace.
unfreeze = Freezer.unfreeze