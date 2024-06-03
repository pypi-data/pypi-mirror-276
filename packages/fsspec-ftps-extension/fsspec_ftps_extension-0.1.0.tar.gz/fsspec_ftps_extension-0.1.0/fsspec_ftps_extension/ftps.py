from ftplib import FTP_TLS

from fsspec.implementations.ftp import FTPFileSystem


class FTPSFileSystem(FTPFileSystem):
    def _connect(self):
        self.ftp = FTP_TLS(timeout=self.timeout)
        self.ftp.connect(self.host, self.port)
        self.ftp.login(*self.cred)
        self.ftp.prot_p()
