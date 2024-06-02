import platform
import re

class _Callback:
    @staticmethod
    def is_win_wine():
        try:
            import ctypes.util # noqa: E402
            return is_wine_dll(ctypes.util.find_library('kernel32'))
        except Exception:
            return False
        
# The below compatibility functions were taken from PyInstaller's compat file.
# https://github.com/pyinstaller/pyinstaller/blob/develop/PyInstaller/compat.py

# Wine detection and support
def is_wine_dll(filename):
    """
    Check if the given PE file is a Wine DLL (PE-converted built-in, or fake/placeholder one).

    Returns True if the given file is a Wine DLL, False if not (or if file cannot be analyzed or does not exist).
    """

    _WINE_SIGNATURES = (
        b'Wine builtin DLL',  # PE-converted Wine DLL
        b'Wine placeholder DLL',  # Fake/placeholder Wine DLL
    )
    _MAX_LEN = max([len(sig) for sig in _WINE_SIGNATURES])

    # Wine places their DLL signature in the padding area between the IMAGE_DOS_HEADER and IMAGE_NT_HEADERS. So we need
    # to compare the bytes that come right after IMAGE_DOS_HEADER, i.e., after initial 64 bytes. We can read the file
    # directly and avoid using the pefile library to avoid performance penalty associated with full header parsing.
    try:
        with open(filename, 'rb') as fp:
            fp.seek(64)
            signature = fp.read(_MAX_LEN)
        return signature.startswith(_WINE_SIGNATURES)
    except Exception:
        pass
    return False

def _pyi_machine(machine, system):
    """
    Choose an intentionally simplified architecture identifier to be used in the bootloader's directory name.

    Args:
        machine:
            The output of ``platform.machine()`` or any known architecture alias or shorthand that may be used by a
            C compiler.
        system:
            The output of ``platform.system()`` on the target machine.
    Returns:
        Either a string tag or, on platforms that don't need an architecture tag, ``None``.

    Ideally, we would just use ``platform.machine()`` directly, but that makes cross-compiling the bootloader almost
    impossible, because you need to know at compile time exactly what ``platform.machine()`` will be at run time, based
    only on the machine name alias or shorthand reported by the C compiler at the build time. Rather, use a loose
    differentiation, and trust that anyone mixing armv6l with armv6h knows what they are doing.
    """
    # See the corresponding tests in tests/unit/test_compat.py for examples.

    if platform.machine() == "sw_64" or platform.machine() == "loongarch64":
        # This explicitly inhibits cross compiling the bootloader for or on SunWay and LoongArch machine.
        return platform.machine()

    if system == "Windows":
        if machine.lower().startswith("arm"):
            return "arm"
        else:
            return "intel"

    if system != "Linux":
        # No architecture specifier for anything par Linux.
        # - macOS is on two 64 bit architectures, but they are merged into one "universal2" bootloader.
        # - BSD supports a wide range of architectures, but according to PyPI's download statistics, every one of our
        #   BSD users are on x86_64. This may change in the distant future.
        return

    if machine.startswith(("arm", "aarch")):
        # ARM has a huge number of similar and aliased sub-versions, such as armv5, armv6l armv8h, aarch64.
        return "arm"
    if machine in ("thumb"):
        # Reported by waf/gcc when Thumb instruction set is enabled on 32-bit ARM. The platform.machine() returns "arm"
        # regardless of the instruction set.
        return "arm"
    if machine in ("x86_64", "x64", "x86"):
        return "intel"
    if re.fullmatch("i[1-6]86", machine):
        return "intel"
    if machine.startswith(("ppc", "powerpc")):
        # PowerPC comes in 64 vs 32 bit and little vs big endian variants.
        return "ppc"
    if machine in ("mips64", "mips"):
        return "mips"
    if machine.startswith("riscv"):
        return "riscv"
    # Machines with no known aliases :)
    if machine in ("s390x",):
        return machine

    # Unknown architectures are allowed by default, but will all be placed under one directory. In theory, trying to
    # have multiple unknown architectures in one copy of PyInstaller will not work, but that should be sufficiently
    # unlikely to ever happen.
    return "unknown"