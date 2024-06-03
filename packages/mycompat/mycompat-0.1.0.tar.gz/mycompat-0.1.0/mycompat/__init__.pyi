is_64bits: bool

is_py33: bool
is_py34: bool
is_py35: bool
is_py36: bool
is_py37: bool
is_py38: bool
is_py39: bool
is_py310: bool
is_py311: bool
is_py312: bool

is_win: bool
is_win_10: bool
is_win_11: bool
is_win_wine: bool

is_cygwin: bool
is_darwin: bool

is_linux: bool
is_solar: bool
is_aix: bool
is_freebsd: bool
is_openbsd: bool
is_hpux: bool

is_unix: bool
is_musl: bool

_macos_ver: tuple[int, int, int] | None

is_macos_11: bool
is_macos_11_compat: bool
is_macos_11_native: bool

base_prefix: str

is_venv: bool
is_virtualenv: bool

is_conda: bool
is_pure_conda: bool

python_executable: str
is_ms_app_store: bool

machine: str
architecture: str
simple_machine: str

is_frozen: int

def unfreeze() -> None: ...