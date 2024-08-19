import os
from typing import List
from logging import getLogger

logger = getLogger(__name__)


class FolderTruant:
    def __init__(self, path: str):
        self.path = path
        self.inner_files_paths: List[str] = self._get_inner_files_paths()
        logger.info(f"После обхода вложенных папок : Количество файлов  {len(self.inner_files_paths)}")

    def _get_inner_files_paths(self) -> List[str]:
        """
        Проходит по всем вложенным подпапкам и возвращает список путей ко всем файлам
        """
        paths_inner_files = [
            os.path.join(root, file) for root, _, files in os.walk(self.path) for file in files
        ]
        return paths_inner_files
