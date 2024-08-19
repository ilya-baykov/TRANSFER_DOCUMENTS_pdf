from dataclasses import dataclass


@dataclass
class RequestsParameters:
    """Датакласс с параметрами для запросов к ЕИП"""
    nameDoc: str  # Имя файла с расширением. Пример заполнения - Иванов Иван Иванович_642000036171.xlsx
    dateDoc: str  # Поле «Дата подписания». Пример заполнения - 2022-04-17T10:00:00.000Z
    account: str  # Лицевой счет клиента (Поле «Лицевой счет»)
    initiator: str  # ФИО отправившего в Архив (АПД), (по наименованию папки)
    inn: str  # ИНН (поле «ИНН»)
    contractNumber: str  # Поле «Номер договора»
    clientName: str  # Поле «Наименование клиента»
    segmentDoc: str = "B2B"  # Сегмент, по умолчанию - B2B
    typeDoc: str = "actLossDD"  # Вид документа, по умолчанию actLossDD
    systemSend: str = "5"  # Заполняется системой отправителем. Для отправки через ЕИП использовать "5"
