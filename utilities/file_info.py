import os
from logging import getLogger
logger = getLogger(__name__)


class FileInfo:
    def __init__(self, file_path):
        self.name = os.path.basename(file_path)
        self.name_without_extension, self.extension = os.path.splitext(os.path.basename(file_path))
        self.root_fullname = os.path.basename(os.path.dirname(file_path))  # ФИО сотрудника из папки с файлом
        self.directory_path = os.path.dirname(os.path.abspath(file_path))  # путь к директории, где находится файл
        self.path_save_xlsx = os.path.join(self.directory_path, self.name_without_extension + '.xlsx')
        self.path = file_path  # Путь к файлу
        logger.info(f"Была получена информация по файлу {file_path}")

