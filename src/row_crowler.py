from config.handbook import HandbookIndex
from exeptions import RowValidateError
from validators.row_validate import *


class RowHandler:
    """Класс для обработки строки"""

    def __init__(self, row: RowDataFrame):
        """При успешной валидации данных инициализирует объект строки"""
        filling_row_validator = FillingRowValidator(row)  # Объект для проверки заполнения строки
        self.filled_fields = filling_row_validator.filled_fields  # Получаем заполненные поля строки
        if filling_row_validator.check():
            self.row = row  # Инициализируем объект строк при успешной проверки
            self.handbook_index_obj = HandbookIndex(account=row.account)  # Объект справочника для получения филиала
        else:
            self.row = None

    def get_error_message(self) -> List[str]:
        """Возвращает список всех ошибок в строке"""
        try:
            error_collector = ErrorCollector(
                AccountLengthValidator(account=self.row.account),
                AccountDigitValidator(account=self.row.account),
                BranchValidator(handbook_indexes=self.handbook_index_obj.indexes)
            ).get_errors()

            if error_collector:
                loger.error(
                    f"При проверки таблицы в строке #{self.row.line_number}: ЛС {self.row.account}"
                    f" были получены такие ошибки {error_collector}")
            return error_collector
        except Exception as e:
            raise RowValidateError
