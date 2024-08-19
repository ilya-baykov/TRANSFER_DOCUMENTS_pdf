import datetime
import sys

from logging import basicConfig, DEBUG
from config.handbook import ReferenceData
from config.paths import PATH_DELETE
from reporting_files.report_file import report_file
from reporting_files.report_dataclass import ReportRowData
from requestsEIP.document_id import RequestGetDocumentId
from requestsEIP.request_card_status import RequestCardStatus
from requestsEIP.request_parameters import RequestsParameters
from src.file_transfer import FileTransfer
from src.row_crowler import RowHandler
from utilities.launch_preparation import LaunchPreparer
from src.file_crawler import FileCrawler

from validators.row_validate import *
from utilities.row_info import RowDataFrame

loger = getLogger()
LOGER_FORMAT = "%(asctime)s : %(name)s : %(levelname)s - %(message)s"
basicConfig(level=DEBUG, format=LOGER_FORMAT)

if __name__ == '__main__':
    loger.info("Скрипт Запущен")
    if not LaunchPreparer().is_ready_launch():  # Проверка наличия доступа ко всем нужным сетевым ресурсам
        loger.error("Возникли проблемы с наличием или доступам к необходимым сетевым ресурсам")
        sys.exit()
    for file, table_rows_df, date_headers in FileCrawler().bypass_files():  # Получение информации по текущему pdf файлу
        for _index, _row in table_rows_df.iterrows():

            # Заполняем поля объекта ReportRowData для дальнейшей записи в отчёт
            report_row_data = ReportRowData(employee_fullname=file.root_fullname, registry=file.name,
                                            document_date=date_headers)

            # Инициализация строки таблицы
            row_handler = RowHandler(row=RowDataFrame(_row))
            report_row_data.fill_fields(filled_fields=row_handler.filled_fields)  # Заполняем поля отчёта

            # Проверка на заполненность полей в строке таблицы
            if row_handler.row is None:
                report_row_data.status, report_row_data.error_comment = "Ошибка", "Отсутствуют атрибуты к обработке"
                report_file.create_row(columns_data=report_row_data)
                continue

            # Проверка на валидность значений в строке таблицы
            row_error_message = row_handler.get_error_message()  # Проверка корректности данных из таблицы
            if row_error_message:
                report_row_data.status, report_row_data.error_comment = "Ошибка", ",".join(row_error_message)
                report_file.create_row(columns_data=report_row_data)
                continue

            # Получение данных из мэппинга филиалов
            try:
                reference_data: ReferenceData = row_handler.handbook_index_obj.get_handbook_row_data()
                branch, branch_id = reference_data.branch, reference_data.branch_id
                report_row_data.branch = branch
            except Exception as e:
                loger.error(f"При попытке получить филиал для {row_handler.row.account} произошла ошибка {e}")
                report_row_data.status, report_row_data.error_comment = "Ошибка", "Ошибка получения филиала"
                report_file.create_row(columns_data=report_row_data)
                continue

            # Формирование данных для запросов к ЕИП
            request_parameters = RequestsParameters(
                nameDoc=row_handler.row.document_name, dateDoc=date_headers,
                account=row_handler.row.account, initiator=file.root_fullname,
                inn=row_handler.row.inn, contractNumber=row_handler.row.document_number,
                clientName=row_handler.row.document_date
            )

            # Запрос для получения id документа
            report_row_data.processing_start_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            # document_id = RequestGetDocumentId(branch_id=branch_id, data=request_parameters).get_document_id()
            document_id = None
            if document_id:

                report_row_data.document_id = document_id
                report_row_data.processing_end_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

                # Запрос для проверки статуса загрузки
                if RequestCardStatus(branch_id, document_id, request_parameters.nameDoc, file.path).check_card_status():
                    report_row_data.status = "Выполнено"
                else:
                    report_row_data.status, report_row_data.error_comment = "Ошибка", "Документ не загружен"

            else:
                report_row_data.status, report_row_data.error_comment = "Ошибка", "Карточка не создана"

            report_file.create_row(columns_data=report_row_data)

            # # Копирование и перенос в корзину исходного файла
            # file_handler = FileTransfer(file.path, file.directory_path, row_handler.row.account)
            # file_handler.copy_file(PATH_DELETE)

    report_file.save()
    print("Конец программы")
    loger.info("Скрипт завершил свою работу")
