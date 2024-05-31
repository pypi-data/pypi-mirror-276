from ralium.api import (
    _check_web_folder,
    _check_web_routes
)

from ralium._util import (
    SYS_BUNDLE_ATTRIBUTE,
    SYS_PATH_SEPERATOR,
    BACKSLASH,
    _get_bundle,
    _get_path,
    _norm_url
)

from shutil import COPY_BUFSIZE
from http import HTTPStatus

import urllib.parse
import http.server
import posixpath
import os

IMAGE_FILE_EXTENSIONS = [
    ".apng", ".gif", ".ico", ".cur", ".jpg", ".jpeg", 
    ".jfif", ".pjpeg", ".pjp", ".png", ".svg", ".ico",
    ".webp"
]

# A modified version of http.server.SimpleHTTPRequstHandler
# made compatible with the custom 'FileSystem' class.
class BundledHTTPServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f is not None:
            try:
                self.copyfile(f, self.wfile)
            except:
                return

    def do_HEAD(self):
        """Serve a HEAD request."""
        self.send_head()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        f = None
        path = self.translate_path(self.path)
        ctype = self.guess_type(path)
        # check for trailing "/" which should return 404. See Issue17324
        # The test for this was added in test_httpserver.py
        # However, some OS platforms accept a trailingSlash as a filename
        # See discussion on python-dev and Issue34711 regarding
        # parsing and rejection of filenames with a trailing slash
        if path.endswith("/"):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            f = _get_bundle().open(path)
        except FileNotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        try:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(len(str(f))))
            self.end_headers()
            return f
        except:
            raise
    
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = "\\"
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    def copyfile(self, fsrc, fdst):
        fdst_write = fdst.write
        while buf := fsrc[:COPY_BUFSIZE]:
            fdst_write(buf)

class File:
    __slots__ = ("relpath", "content",)

    def __init__(self, relpath, content):
        self.relpath = relpath
        self.content = content
    
    def __str__(self):
        return self.content.decode()

    def __repr__(self):
        DOUBLE_BACKSLASH = "\\\\"
        return f"ralium.bundle.File(relpath='{self.relpath.replace(BACKSLASH, DOUBLE_BACKSLASH)}', content={repr(self.content)})"
    
class Bundle:
    __slots__ = ("url", "page", "server", "styles",)

    def __init__(self, *, url, page, server, styles):
        self.url = url
        self.page = page
        self.server = server
        self.styles = styles
    
    def __repr__(self):
        return f"ralium.bundle.Bundle(url='{self.url}', page={repr(self.page)}, server={repr(self.server)}, styles=[{''.join([repr(v) for v in self.styles])}])"

class FileSystem:
    __slots__ = ("images", "styles", "bundles", "dirs", "files",)

    def __init__(self, *, images, styles, bundles):
        self.images = images
        self.styles = styles
        self.bundles = bundles

        self.dirs = [SYS_PATH_SEPERATOR]
        self.files = {}

        for image in images:
            self.__add_file(image)

        for style in styles:
            self.__add_file(style)
        
        for bundle in bundles:
            self.__add_file(bundle.page)

            if bundle.server is not None:
                self.__add_file(bundle.server)
            
            for style in bundle.styles:
                self.__add_file(style)
    
    def __add_file(self, file):
        segments = file.relpath.split(SYS_PATH_SEPERATOR)[1:]
        segments = [f"{SYS_PATH_SEPERATOR}{SYS_PATH_SEPERATOR.join([*segments[:i], v])}" for i, v in enumerate(segments)]

        self.mkdirs(*segments[:-1])
        self.mkfiles(**{segments[-1]: file.content})

    def open(self, filename):
        try:
            return self.files[filename]
        except KeyError:
            raise FileNotFoundError(f"'{filename}' does not exist.")
    
    def exists(self, path):
        if self.files.get(path) is not None:
            return False
        return path in self.dirs

    def mkdirs(self, *dirs):
        self.dirs.extend(dirs)
    
    def mkfile(self, filename, data):
        if not isinstance(filename, str):
            raise TypeError(f"File name must be of type str, intead got '{type(filename)}'")
        
        if not isinstance(data, bytes):
            raise TypeError(f"File content must be of type bytes, instead got '{type(data)}'.")

        self.files[filename] = data
    
    def mkfiles(self, **files):
        for filename, data in files.items():
            self.mkfile(filename, data)

class PyBundler:
    __slots__ = ("pyfile", "webfolder", "webroutes", "cssfolder", "imgfolder",)

    def __init__(self, pyfile, webfolder):
        self.pyfile = pyfile
        self.webfolder = _get_path(webfolder)
        self.webroutes = os.path.normpath(os.path.join(self.webfolder, "routes"))
        self.cssfolder = os.path.normpath(os.path.join(self.webfolder, "styles"))
        self.imgfolder = os.path.normpath(os.path.join(self.webfolder, "images"))

        _check_web_folder(self.webfolder)
        _check_web_routes(self.webroutes)

    def view(self):
        images = self.collect(self.imgfolder, PyBundler.isimage)
        styles = self.collect(self.cssfolder, PyBundler.iscss)
        bundles = []

        for root, _, files in os.walk(self.webroutes):
            _url = _norm_url(root.split(self.webroutes)[-1])
            _page = None
            _server = None
            _styles = []

            for file in files:
                filepath = os.path.abspath(os.path.join(root, file))
                filename = os.path.basename(file)
                relpath = self.relpath(filepath)

                match filename:
                    case "+page.html":
                        _page = File(relpath, self.get_content(filepath))
                    case "+server.py":
                        _server = File(relpath, self.get_content(filepath))
                    case _:
                        if not PyBundler.iscss(filename): continue
                        _styles.append(File(relpath, self.get_content(filepath)))
            
            bundles.append(Bundle(url=_url, page=_page, server=_server, styles=_styles))
        
        return [
            b"import ralium.bundle\n",
            b"import sys\n",
            f"setattr(sys, '{SYS_BUNDLE_ATTRIBUTE}', ralium.bundle.FileSystem(\n".encode(),
            f"    images = {images},\n".encode(),
            f"    styles = {styles},\n".encode(),
            f"    bundles = {bundles}\n".encode(),
            b"))\n\n",
            self.get_content(self.pyfile)
        ]
    
    def relpath(self, filename):
        return os.path.normpath(os.path.abspath(filename).removeprefix(os.path.dirname(self.webfolder)))

    def collect(self, dir, callback):
        data = []

        for root, _, files in os.walk(dir):
            for file in files:
                filepath = os.path.abspath(os.path.join(root, file))
                if not callback(filepath): continue

                data.append(File(self.relpath(filepath), PyBundler.get_content(filepath)))
        
        return data

    @staticmethod
    def iscss(filename):
        _, ext = os.path.splitext(filename)
        return ext == ".css"
    
    @staticmethod
    def isimage(filename):
        _, ext = os.path.splitext(filename)
        return ext in IMAGE_FILE_EXTENSIONS
    
    @staticmethod
    def get_content(filename):
        if not os.path.exists(filename):
            return
        
        with open(filename, "rb") as f:
            return f.read()