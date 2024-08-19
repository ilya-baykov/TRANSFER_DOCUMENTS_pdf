from logging import getLogger

from config.constants import MONTH_RU

logger = getLogger(__name__)


class DateFormater:
    def __init__(self, date: str):
        self.date_from_document = date.lower().strip()
        self.date_for_report = self.__date_format()

    def __date_format(self):
        """Заменяет в дате название месяца на номер месяца"""
        for month_name, month_number in MONTH_RU.items():
            if month_name in self.date_from_document:
                return self.date_from_document.replace(month_name, month_number)
        return self.date_from_document

    def get_date(self) -> str:
        """Возвращает дату в определенном шаблоне"""

        try:
            date_elem = self.date_for_report.split()
            year = date_elem[2] if len(date_elem[2]) == 4 else "20" + date_elem[2]
            clear_date = year + '-' + date_elem[1] + '-' + date_elem[0] + 'T00:00:00.000Z'
            logger.info(f"Дата из заголовка - {self.date_from_document} преобразовалась в : {clear_date}")
            return clear_date
        except Exception as e:
            logger.error(f"При попытке форматировать дату из заголовка произошла ошибка - {e}")
            return None
