from docx import Document
from pdf2docx import Converter
from logging import getLogger

logger = getLogger(__name__)


class DocxCreator:
    """Класс для создания объекта документа docx_handler"""

    def __init__(self, file_path: str):
        """
        Создание объекта
        :param file_path: Путь к pdf файлу
        """
        self.pdf_file_path = file_path
        self.docx_file_path = file_path.replace('.pdf', '.docx')
        self.document = self.__pdf_to_docx_converter()

    def __pdf_to_docx_converter(self) -> Document:
        """Конвертирует pdf файл в docx_handler и возвращает объект документа"""
        try:
            cv = Converter(self.pdf_file_path)
            cv.convert(self.docx_file_path, start=0, end=None)
            cv.close()
            logger.info(f"Из файла {self.pdf_file_path}  был получен docx файл")
            return Document(self.docx_file_path)
        except Exception:
            logger.info(f"Ошибка при попытке сконвертировать файл {self.pdf_file_path}")
            return None
