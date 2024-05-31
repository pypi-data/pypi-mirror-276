from ._execute import execute_python as execute_python
from .pyinstaller import PackageInstaller as PackageInstaller, PyInstaller as PyInstaller
from collections import deque
from enum import IntEnum
from typing import Any, Final

class SmartAutoModuleCombineMode(IntEnum):
    DISABLE: Final[int]
    FOLDER_ONLY: Final[int]
    ALL_INTO_ONE: Final[int]

class Builder:
    __PATH: Final[str]
    __CACHE_NEED_REMOVE: Final[tuple[str, ...]]
    CACHE_NEED_REMOVE: Final[deque[str]]
    __DIST_DIR: Final[str]
    @classmethod
    def __remove_cache(cls, path: str) -> None: ...
    @staticmethod
    def remove(*path: str, cwd: str | None = None) -> None: ...
    @classmethod
    def copy(cls, files: tuple[str, ...], target_folder: str, move: bool = False) -> None: ...
    @classmethod
    def copy_tree(cls, src: str, dest: str, move: bool = False, ignore_pattern: str = '') -> None: ...
    @classmethod
    def copy_repo(cls, src: str, dest: str, move: bool = False) -> None: ...
    @classmethod
    def __clean_up(cls) -> None: ...
    @classmethod
    def __combine(cls, _dir_path: str) -> None: ...
    @classmethod
    def compile(cls, source_folder: str, target_folder: str = 'src', additional_files: tuple[str, ...] = ..., ignore_key_words: tuple[str, ...] = ..., smart_auto_module_combine: SmartAutoModuleCombineMode = ..., remove_building_cache: bool = True, update_the_one_in_sitepackages: bool = False, include_pyinstaller_program: bool = False, options: dict[str, Any] = {}) -> None: ...
    @classmethod
    def build(cls) -> None: ...
    @classmethod
    def upload(cls, confirm: bool = True) -> None: ...
