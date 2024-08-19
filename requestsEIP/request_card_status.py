from logging import getLogger

import requests
from requests import Response
from config.constants import HEADERS_FOR_CHECK_CARD_STATUS, BASE_URL as BASE_URL_FROM_CONFIG

loger = getLogger()


class RequestCardStatus:
    BASE_URL = BASE_URL_FROM_CONFIG
    HEADERS = HEADERS_FOR_CHECK_CARD_STATUS

    def __init__(self, branch_id, document_id: str, nameDoc: str, path_file: str):
        """
        Создает запрос к ЕИП для проверки статуса создания карточки
        :param branch_id: Код филиала согласно мэппингу
        :param document_id: id документа, полученного после запроса к ЕИП
        :param nameDoc: Наименование документа
        :param path_file: Путь к файлу
        """
        self.branch_id = branch_id
        self.document_id = document_id
        self.name_doc = nameDoc
        self.path_file = path_file

        self.files = self.__get_file()
        self.response: Response = self.__create_request()

    def __get_file(self):
        with open(self.path_file, 'rb') as file:
            files = {'file': (self.name_doc, file, 'application/pdf')}
        return files

    def __create_request(self) -> Response | None:
        """Отправляем запрос с указанным кодом филиала"""
        try:
            url = (
                    RequestCardStatus.BASE_URL +
                    f"/FWS/datatransfer-facade-rest/digital-archive/file-doc/{self.branch_id}/{self.document_id}/send")

            response = requests.request(method="POST", url=url,
                                        headers=RequestCardStatus.HEADERS, files=self.files)
            return response
        except Exception as e:
            loger.error(f"Ошибка при отправке запроса для проверки корректности загрузки файла в ЕИП - {e}")
            return None

    def check_card_status(self):
        """Метод проверяющий корректность загрузки файла в ЕИП"""
        if isinstance(self.response, Response):
            if self.response.status_code == 200:
                return True
            loger.error(f"Статус запроса для проверки корректности загрузки файла в ЕИП {self.response.status_code} ")
        return None
