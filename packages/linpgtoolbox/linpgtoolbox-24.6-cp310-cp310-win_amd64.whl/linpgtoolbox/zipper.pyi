import zipfile
from typing import Final

class Zipper:
    SCRIPT_EXTENSION: Final[str]
    @classmethod
    def execute(cls, _dir: str = '.') -> None: ...
    @classmethod
    def __zip(cls, _zipFile: zipfile.ZipFile, _path: str) -> None: ...
