import sys
from logging import getLogger

import pandas as pd

from config.paths import PATH_FILES
from reporting_files.report_dataclass import ReportRowData
from reporting_files.report_file import report_file
from src.file_dataframe_builder import DocxTableExtractor
from src.folder_truant import FolderTruant
from src.table_dataframe import TableDataFrameCreator
from utilities.file_info import FileInfo
from validators.file_validate import CheckFileExtension
from validators.table_dataframe_validate import CheckColumnNumbers, CheckColumnNames

logger = getLogger(__name__)


class FileCrawler:
    """Класс для обхода файлов"""

    _instance = None
    _inner_files_paths = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FileCrawler, cls).__new__(cls)
            cls._inner_files_paths = FolderTruant(path=PATH_FILES).inner_files_paths
        return cls._instance

    @classmethod
    def bypass_files(cls):
        """Прохождение по всем найденным файлам"""
        for _file in cls._inner_files_paths:
            file = FileInfo(_file)
            # Проверки валидности файла
            if CheckFileExtension(file).is_valid():
                docx_table_extractor = DocxTableExtractor(file)  # Объект обработчик docx документа
                date_headers: str | None = docx_table_extractor.get_file_headers_date()  # Дата из заголовка
                table_rows_df: pd.DataFrame = TableDataFrameCreator(docx_table_extractor.get_docx_blocks()).get_df()

                if all([table_validators.is_valid(table_rows_df.columns.tolist())
                        for table_validators in (CheckColumnNumbers(file), CheckColumnNames(file))]) and date_headers:
                    yield file, table_rows_df, date_headers
            else:
                # При неправильном расширении файла создается новая строка в отчёте
                report_file.create_row(ReportRowData(employee_fullname=file.root_fullname, registry=file.name,
                                                     status="Ошибка", error_comment="Некорректный формат документа"))
