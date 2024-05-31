from ralium.bundle import BundledHTTPServer, FileSystem

from typing import (
    TypeAlias, 
    Callable, 
    TypeVar, 
    Literal,
    Self, 
    Any, 
)

from types import (
    FunctionType, 
    ModuleType
)

import http.server

__all__ = [
    "__version__", "SYS_PATH_SEPERATOR", "SYS_PATH_SEPERATOR", "BACKSLASH", "BasicHTTPServer", "NamedDict", 
    "_get_http_server_handler", "_get_bundle", "_norm_url", "_norm_path", "_check_exists",  
    "_check_is_dir", "_read_file", "_get_path"
]

__version__: str

BACKSLASH: Literal["\\"]
SYS_BUNDLE_ATTRIBUTE: str
SYS_PATH_SEPERATOR: Literal["\\"] | Literal["/"]

_RT = TypeVar("_RT") # Return Type
ClassType: TypeAlias = object
DirPathStr: TypeAlias = str
FilePathStr: TypeAlias = str

class BasicHTTPServer(http.server.SimpleHTTPRequestHandler): ...

class NamedDict(dict):
    def __init__(self, iterable: dict[str, Any]) -> None: ...
    def __getattr__(self, name: str) -> Any: ...

def _is_abs_win(path: str) -> bool: ...
def _get_bundle() -> FileSystem | None: ...
def _get_http_server_handler() -> BasicHTTPServer | BundledHTTPServer: ...
def _check_exists(path: str) -> bool: ...
def _check_is_dir(path: str) -> bool: ...
def _norm_url(path: str) -> str: ...
def _norm_path(path: str) -> str: ...
def _read_file(path: str, encoding: str = "UTF-8") -> str: ...
def _get_path(path: str) -> str: ...