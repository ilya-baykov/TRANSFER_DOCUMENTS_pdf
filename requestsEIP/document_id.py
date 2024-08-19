from logging import getLogger
from requests import request, Response
from config.constants import HEADERS_FOR_GET_ID_DOCUMENT, BASE_URL as BASE_URL_FROM_CONFIG
from requestsEIP.request_parameters import RequestsParameters

loger = getLogger()


class RequestGetDocumentId:
    """Класс для запроса к ЕИП для получения id документа"""
    BASE_URL = BASE_URL_FROM_CONFIG
    HEADERS = HEADERS_FOR_GET_ID_DOCUMENT

    def __init__(self, branch_id, data: RequestsParameters):
        """
        Создаёт url для POST запроса
        :param branch_id: Номер филиала, согласно мэппингу
        """
        self.branch_id = branch_id
        self.data = data

        self.response: Response = self.__create_request()
        self.document_id = self.get_document_id()

    def __create_request(self) -> Response | None:
        """Отправляем запрос с указанным кодом филиала"""
        try:
            url_send_meta = (RequestGetDocumentId.BASE_URL +
                             f"/FWS/datatransfer-facade-rest/digital-archive/meta-docb2b/{self.branch_id}/send")

            response = request(method="POST", url=url_send_meta,
                               headers=RequestGetDocumentId.HEADERS, data=self.data)
            return response
        except Exception as e:
            loger.error(f"При попытке получить id документа для кода филиала:{self.branch_id} произошла ошибка {e}")
            return None

    def get_document_id(self) -> str | None:
        """Возвращает id документа при успешном запросе, иначе возвращает - None """
        if isinstance(self.response, Response):
            if self.response.status_code == 200:
                try:
                    document_id = self.response.json()['iDocument']
                    return str(document_id)
                except Exception as e:
                    loger.error(f"В запросе не было информации об id-документа {e} ")
                    return None
        return None
