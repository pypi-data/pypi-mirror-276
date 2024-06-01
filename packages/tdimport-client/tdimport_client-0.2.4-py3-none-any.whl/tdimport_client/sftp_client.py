import logging
import pathlib
import warnings
import pysftp
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class TDBundleUploadSFTPClient:
    bundle: pathlib.Path
    host: str
    username: str
    password: str = field(repr=False)
    is_success: bool = field(default=False, init=False)

    UPLOAD_PATH = "/D:/td-bundles"

    @property
    def bundle_upload_path(self) -> str:
        return f"{self.UPLOAD_PATH}/{self.bundle.name}"

    def push(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._push()

    def _push(self) -> None:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        sftpkw = dict(username=self.username, password=self.password, cnopts=cnopts)
        with pysftp.Connection(self.host, **sftpkw) as sftp:
            sftp.chdir(self.UPLOAD_PATH)
            result = sftp.put(self.bundle)
            logger.info(f"SFTP result: {result}, for file: {self.bundle}")
        self.is_success = True
