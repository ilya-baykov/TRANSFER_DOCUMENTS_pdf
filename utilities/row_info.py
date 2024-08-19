from logging import getLogger

import pandas as pd

from config.constants import COLUMN_MAPPING

loger = getLogger()


class RowDataFrame:
    """Класс для инкапсуляции данных"""

    def __init__(self, row: pd.Series):
        """Считывание названия столбцов"""
        self.row = row
        self.client_name = self.inn = self.document_number = self.document_date = self.line_number = self.account = None
        self.__fill_fields()
        self.document_name = self.__forming_document_name()

    def __fill_fields(self):
        """Заполнение всех полей с учётом мэппинга"""
        for attr, possible_names in COLUMN_MAPPING.items():
            setattr(self, attr,
                    self.__get_value_from_possible_names(possible_names,
                                                         'Название столбца не совпадает с шаблоном'))

    def __get_value_from_possible_names(self, possible_names: list, default_message: str):
        """Получение значения из возможных названий столбцов"""
        for name in possible_names:
            if name in self.row:
                return str(self.row[name]).strip()
        return default_message

    def __forming_document_name(self) -> str | None:
        """Формирует имя документа на основе лицевого счёта и номера строки в таблице"""
        if self.account:
            if self.line_number:
                return f"{self.account}_{self.line_number}.pdf"
            else:
                return f"{self.account}_НЕИЗВЕСТНЫЙ_НОМЕР_СТРОКИ.pdf"
        return None

    def __iter__(self):
        """Магический метод для итерации по полям"""
        return iter([
            ("Номер строки в исходной таблице", self.line_number),
            ("Наименование клиента", self.client_name),
            ("ИНН", self.inn),
            ("Лицевой счет", self.account),
            ("Номер договора", self.document_number),
            ("Дата договора", self.document_date),
            ("Наименование документа", self.document_name)
        ])

    def __len__(self):
        """Возвращает количество полей"""
        return sum(1 for _ in [self.line_number, self.client_name, self.inn,
                               self.account, self.document_number, self.document_date, self.document_name])
