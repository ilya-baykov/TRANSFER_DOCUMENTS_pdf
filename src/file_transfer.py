import os
import shutil
from logging import getLogger

loger = getLogger()


class FileNameGenerator:
    def __init__(self, directory_path: str, account: str) -> None:
        """
        Инициализация генератора имен файлов.

        :param directory_path: Путь к директории, где будут сохраняться файлы.
        :param account: Лицевой счет, который будет использоваться в имени файла.
        """
        self.directory_path = directory_path
        self.account = account

    def create_unique_file_name(self) -> str:
        """
        Создает уникальное имя файла, добавляя индекс, если файл с таким именем уже существует.

        :return: Уникальное имя файла.
        """
        base_file_name = f"{self.account}.pdf"
        new_file_name = base_file_name
        index = 1

        # Проверяем, существует ли файл, и если да, добавляем индекс
        while os.path.exists(os.path.join(self.directory_path, new_file_name)):
            new_file_name = f"{self.account}_{index}.pdf"
            index += 1

        return new_file_name


class FileTransfer:
    def __init__(self, file_path: str, directory_path: str, account: str) -> None:
        """
        Инициализация обработчика файлов.

        :param file_path: Путь к исходному файлу, который нужно скопировать.
        :param directory_path: Путь к директории, где будет сохранен файл.
        :param account: Лицевой счет, который будет использоваться в имени файла.
        """
        self.file_path = file_path
        self.directory_path = directory_path
        self.account = account
        self.file_name_generator = FileNameGenerator(directory_path, account)

    def copy_file(self, delete_path: str) -> None:
        """
        Копирует файл в указанную директорию с уникальным именем и удаляет оригинал.

        :param delete_path: Путь, куда будет скопирован оригинал файла для удаления.
        """
        try:
            # new_file_name = self.file_name_generator.create_unique_file_name()
            # new_file_path = os.path.join(self.directory_path, new_file_name)
            # shutil.copy2(self.file_path, new_file_path)  # Копируем файл в новую директорию

            shutil.copy2(self.file_path, delete_path)  # Копируем файл в директорию для удаления
        except Exception as e:
            loger.error(f"Во время копирования файла {self.file_path} произошла ошибка {e}")
