import re
from typing import List
from logging import getLogger
from docx.table import Table
from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from exeptions import TypeErrorTable, TypeErrorDocx

logger = getLogger(__name__)


class DocumentHandler:

    def __init__(self, docx_document: _Document):
        self.docx_document = docx_document

    def __iter_block_items(self):
        """
        Генерирует ссылку на каждый абзац и таблицу внутри объекта document в порядке их появления.
        Возвращает:
            Generator[Union[Paragraph, Table], None, None]: Каждый дочерний элемент типа Paragraph или Table в порядке их появления.

        Исключения:
            TypeErrorDocx: Если   self.docx_documen не является _Document.
        """
        if isinstance(self.docx_document, _Document):
            parent_elm = self.docx_document.element.body
        else:
            raise TypeErrorDocx

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_Tbl):
                yield Table(child, self.docx_document)

    def get_year_from_docx_paragraph(self) -> str | None:
        """Возврвщает год документа из шапки файла"""
        for para in self.docx_document.paragraphs:
            match = re.search(r"«(\d{1,2})»[\s_]+(\w+)[\s_]+(\d{4}|\d{2})", str(para.text))
            if match:
                row_date_str = match.group(0)  # Извлекаем найденную подстроку
                logger.info(f"Дата в шапке докумена {row_date_str}")
                return row_date_str.replace('«', '').replace('»', '').replace(' г.', '')
        logger.error("В шапке документа не была обнаружена дата")
        return None

    def through_blocks(self) -> List[List[str]]:
        """Метод для обхода блоков документа
           Возвращает вложенный список с текстом всех ячеек всех таблиц
        """
        rows_table_info = []
        for block in self.__iter_block_items():
            if block:
                table = TableDoc(block)
                rows_table_info.extend(table.through_rows())
        logger.info(f"Таблица в документе была считана, её размер - {len(rows_table_info)}")
        return rows_table_info


class TableDoc:
    def __init__(self, table: Table):
        """

        :param table: Таблица - объект  Table из docx_handler.table, в противном случае вызывается ошибка TypeErrorTable
        """
        if isinstance(table, Table):
            self.table = table
            self.__total_table_data = []  # Резьлтирующая таблица
        else:
            raise TypeErrorTable

    def through_rows(self):
        """Метод для обхода всех рядов таблицы
           Возвращает вложенный список с текстом ячеек таблицы
        """

        for row in self.table.rows:  # Обход по строкам
            row_data: List[str] = []
            for i, cell in enumerate(row.cells, start=0):  # Обход по ячейкам
                if i == 1 and not self.__check_first_cell(row_data[0].replace(' ', '')):
                    break
                row_data.append(str(cell.text))
            else:
                self.__total_table_data.append(row_data)

        return self.__total_table_data

    def __check_first_cell(self, cell_text: str) -> bool:
        """Метод для проверки текста первой ячейки"""

        return cell_text.isdigit() or ('№' in cell_text)
