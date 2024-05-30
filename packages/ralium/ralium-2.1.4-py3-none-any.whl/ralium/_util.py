import http.server
import string
import sys
import os

__all__ = [
    "__version__", "SYS_PATH_SEPERATOR", "SYS_PATH_SEPERATOR", "BasicHTTPServer", "NamedDict", 
    "_get_http_server_handler", "_get_bundle", "_norm_url", "_norm_path", "_check_exists",  
    "_check_is_dir", "_read_file", "_get_path"
]

__version__ = "2.1.4"

SYS_BUNDLE_ATTRIBUTE = "bundled"
SYS_PATH_SEPERATOR = "\\" if sys.platform.startswith("win") else "/"

class BasicHTTPServer(http.server.SimpleHTTPRequestHandler):
    pass

class NamedDict(dict):
    def __init__(self, iterable):
        for key, value in iterable.items():
            if isinstance(value, dict):
                self[key] = NamedDict(value)
                continue

            self[key] = value

def _is_abs_win(path):
    if not sys.platform.startswith("win"):
        return False

    for letter in string.ascii_uppercase:
        if path.startswith(f"{letter}:"):
            return True

    return False

def _get_bundle():
    return getattr(sys, SYS_BUNDLE_ATTRIBUTE, None)

def _get_http_server_handler():
    if _get_bundle() is not None:
        import ralium.bundle
        return ralium.bundle.BundledHTTPServer
    return BasicHTTPServer

def _check_exists(path):
    path = _norm_path(path)
    bundle = _get_bundle()

    if bundle is not None:
        return bundle.exists(path)
    
    return os.path.exists(path)

def _check_is_dir(path):
    bundle = _get_bundle()

    if bundle is not None:
        return path in bundle.dirs
    
    return os.path.isdir(path)

def _norm_url(path):
    return os.path.normpath(f"/{path.lstrip('/\\')}").replace("\\", "/")

def _norm_path(path):
    if _is_abs_win(path):
        return path
    return os.path.normpath(f"{SYS_PATH_SEPERATOR}{path.lstrip('/\\')}").replace("/", SYS_PATH_SEPERATOR)

def _read_file(path, encoding = "UTF-8"):
    bundle = _get_bundle()

    if bundle is not None:
        return bundle.open(path).decode(encoding)
    
    with open(path, "r", encoding=encoding) as f:
        return f.read()

def _get_path(path):
    bundle = _get_bundle()

    if bundle is not None:
        return _norm_path(path)

    if getattr(sys, "frozen", False):
        return os.path.abspath(os.path.join(sys._MEIPASS, path))

    return os.path.abspath(path.lstrip("\\"))