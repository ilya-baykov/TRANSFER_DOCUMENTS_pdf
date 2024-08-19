import os
import shutil
from datetime import datetime
from logging import getLogger

import pandas as pd

from config.paths import PATH_REPORTS, PATH_TEMPLATE_REPORTS
from reporting_files.report_dataclass import ReportRowData

logger = getLogger(__name__)


class ReportFile:
    """Класс для работы с файлом отчёта"""

    def __init__(self):
        """
        Проверяет наличие файла отчета. Если файл не существует, создает его из шаблона
        """
        self.report_file_path = os.path.join(PATH_REPORTS,
                                             'Отчет робота ' + datetime.now().strftime(
                                                 "%Y-%m-%d") + '_Акт об утере ДД.xlsx')
        if not os.path.exists(self.report_file_path):
            shutil.copy2(PATH_TEMPLATE_REPORTS, self.report_file_path)
            logger.info("Файла отчёта был скопирован из шаблона отчётов")
        self.__report_file_df = pd.read_excel(self.report_file_path,
                                              sheet_name='Отчет робота')  # Перевод в pd.DateFrame
        self.__report_file_df.columns = self.__report_file_df.columns.str.replace('\n', '')  # Удаление переноса строки
        self.__report_file_df.columns = self.__report_file_df.columns.str.strip()

    def row_add(self, columns_data: ReportRowData):
        """
        Добавляет запись в отчёт, записывая только те данные, которые соответствуют существующим колонкам
        :param columns_data: Данные для заполнения {'Название колонки':'Значение'}
        """
        index = len(self.__report_file_df.index)  # Получаем текущий индекс строки
        current_row = self.__report_file_df.loc[index].to_dict()  # Получаем текущую строку в виде словаря

        # Заполняем отсутствующие значения из columns_data в current_row
        for key, value in current_row.items():
            if pd.isna(columns_data.__getattribute__(key)) and not pd.isna(key):
                columns_data.__setattr__(key, value)

        # Создаем новую строку с данными из columns_data, используя __iter__
        new_row = {label: value for label, value in columns_data}

        # Добавляем новую строку в DataFrame
        self.__report_file_df.loc[index] = new_row
        logger.info(f"В отчётный файл в строку {index} была добавлена строка {new_row}")

    def create_row(self, columns_data: ReportRowData):
        index = len(self.__report_file_df.index) + 1  # Получаем индекс для новой строки

        # Создаем новую строку с данными из columns_data, используя __iter__
        new_row = {label: value for label, value in columns_data}

        # Добавляем новую строку в DataFrame
        self.__report_file_df.loc[index] = new_row
        logger.info(f"В отчётный файл была добавлена новая строка:{index}  {new_row}")

    def save(self):
        """Сохраняет отчёт в формате xlsx"""
        try:
            # Сохраняем DataFrame в файл Excel
            self.__report_file_df.to_excel(self.report_file_path, sheet_name='Отчет робота', index=False)
            logger.info(f"Отчёт успешно сохранён в {self.report_file_path}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении отчёта: {e}")


report_file = ReportFile()
