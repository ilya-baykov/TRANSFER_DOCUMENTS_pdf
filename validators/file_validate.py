from abc import ABC, abstractmethod
from logging import getLogger
from utilities.file_info import FileInfo

logger = getLogger(__name__)


class FileValidator(ABC):
    """Абстрактный Класс для валидации файла"""

    def __init__(self, file: FileInfo):
        """
        :param file: Информация по файлу
        """
        self.file = file

    @abstractmethod
    def is_valid(self) -> bool:
        """Возвращает результат проверки файла"""
        pass


class CheckFileExtension(FileValidator):

    def is_valid(self) -> bool:
        """Проверяет расширение файла"""
        if self.file.extension != ".pdf":
            logger.error(f"{self.file.path} Расширение файла отлично от .pdf")
            return False
        return True
