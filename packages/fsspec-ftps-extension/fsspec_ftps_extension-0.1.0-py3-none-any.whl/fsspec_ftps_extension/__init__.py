import fsspec

from .ftps import FTPSFileSystem


fsspec.register_implementation('ftps', FTPSFileSystem)

__all__ = ('FTPSFileSystem', )
