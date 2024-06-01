import logging
import pathlib
import zipfile
import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class TDBundleImportModel(BaseModel):
    Host: str
    userName: str
    password: str
    sourceFile: str
    analyticPackageName: str
    analyticApplications: List[str]
    platformWorkspaceId: str
    platformWorkspaceName: str


class TDBundleImportResponseModel(BaseModel):
    status: str
    message: str
    id: str = "00000000-0000-0000-0000-000000000000"
    started: Optional[datetime.datetime] = None
    created: Optional[datetime.datetime] = None
    updated: Optional[datetime.datetime] = None


class TDBundleUploadModel(BaseModel):
    DatasetId: str
    StartDate: str
    EndDate: str
    TotalPatients: int
    EngineType: str = "TD"
    IsGroupedData: bool = True
    ReferenceFiles: Dict[str, Any] = Field(default_factory=dict)
    TransactionFiles: Dict[str, Any] = Field(default_factory=dict)
    CustomFilterLabels: Dict[str, Any] = Field(default_factory=dict)

    def _mk_fn(self, ext: str) -> str:
        return f"{self.DatasetId}.{ext}"

    def export_to(
        self, dir_path: pathlib.Path, files_path: pathlib.Path
    ) -> pathlib.Path:
        """
        Exports a zip file bundle as a Path, ready for pushing.

        Args:
            dir_path: directory where to save the bundle
            files_path: directory where files are for ReferenceFiles and TransactionFiles
        """
        zip_bundle = dir_path.joinpath(self._mk_fn("zip"))
        files_to_write = [
            *self.ReferenceFiles.values(),
            *self.TransactionFiles.values(),
        ]
        with zipfile.PyZipFile(
            str(zip_bundle), mode="w", compression=zipfile.ZIP_DEFLATED
        ) as zf:
            zf.writestr(self._mk_fn("json"), self.json(by_alias=True))
            for fp in map(files_path.joinpath, files_to_write):
                zf.write(fp, arcname=fp.name)
        logger.info(f"TDBundle created at: {zip_bundle}")
        return zip_bundle
