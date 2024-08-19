from logging import getLogger
from typing import List

from docx_handler.docx_creator import DocxCreator
from docx_handler.docx_document import DocumentHandler
from utilities.date_formater import DateFormater

from utilities.file_info import FileInfo

logger = getLogger(__name__)


class DocxTableExtractor:
    """Класс для создания объекта docx файла и получения текста ячеек таблицы и даты из заголовка """

    def __init__(self, file: FileInfo):
        self.__file = file
        self.__docx_document = DocxCreator(file.path).document  # Объект docx файла, полученного из pdf
        self.__docx_document_handler = DocumentHandler(self.__docx_document)  # Объект обработчика docx документа

    def get_docx_blocks(self) -> List[List[str]]:
        """Возвращает текст ячеек из таблицы в файле в виде вложенного списка строк"""
        return self.__docx_document_handler.through_blocks()

    def get_file_headers_date(self):
        """Возвращает дату из заголовка документа"""
        row_date = self.__docx_document_handler.get_year_from_docx_paragraph()
        if row_date:
            return DateFormater(date=row_date).get_date()
        return None
