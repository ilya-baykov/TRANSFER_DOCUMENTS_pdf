from abc import ABC, abstractmethod
from logging import getLogger
from typing import List

from config.constants import POSSIBLE_NAMES
from utilities.file_info import FileInfo

logger = getLogger(__name__)


class TableDataFrameValidator(ABC):
    """Абстрактный Класс для валидации сформированной таблицы данных из файла"""

    def __init__(self, file: FileInfo):
        """
        :param file: Информация о файле
        """
        self.file = file

    @abstractmethod
    def is_valid(self, columns: List[str]):
        """Возвращает результат проверки табличного датафрейма"""
        pass


class CheckColumnNumbers(TableDataFrameValidator):
    def is_valid(self, columns: List[str]) -> bool:
        """Проверка количества столбцов"""
        number_of_columns = len(columns)
        if 7 >= number_of_columns >= 4:
            logger.info(f"Из таблицы был сформирован DateFrame размерностью {number_of_columns}")
            return True

        logger.error(f"Количество столбцов таблицы : {number_of_columns}")
        return False


class CheckColumnNames(TableDataFrameValidator):
    def is_valid(self, columns: List[str]) -> bool:
        """Проверка названий столбцов на соответствие шаблону"""

        for name in columns:
            if name not in POSSIBLE_NAMES:
                logger.error(f"Столбец с названием '{name}' не соответствует шаблону")
                return False
        logger.info(f"Названия всех столбцов соответствуют шаблону {columns}")
        return True
