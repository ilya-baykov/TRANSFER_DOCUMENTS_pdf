from dataclasses import dataclass, field
from typing import Iterator, Tuple, Dict, Optional


@dataclass
class ReportRowData:
    """Класс с полями заполнений для отчётной таблицы """
    employee_fullname: str
    registry: str
    document_name: Optional[str] = None
    branch: Optional[str] = None
    personal_account: Optional[str] = None
    inn: Optional[str] = None
    contract_number: Optional[str] = None
    contract_date: Optional[str] = None
    document_date: Optional[str] = None
    document_id: Optional[str] = None
    status: Optional[str] = None
    processing_start_date: Optional[str] = None
    processing_end_date: Optional[str] = None
    error_comment: Optional[str] = None

    # Словарь для сопоставления русских названий с именами полей
    labels: Dict[str, str] = field(default_factory=lambda: {
        "ФИО": "employee_fullname",
        "Реестр": "registry",
        "Наименование документа": "document_name",
        "Филиал": "branch",
        "Лицевой счет": "personal_account",
        "ИНН": "inn",
        "Номер договора": "contract_number",
        "Дата договора": "contract_date",
        "Дата документа": "document_date",
        "Id документа - ШК": "document_id",
        "Статус обработки документа роботом": "status",
        "Дата начала обработки (дд.мм.гггг, чч.мм.сс)": "processing_start_date",
        "Дата окончания обработки (дд.мм.гггг, чч.мм.сс)": "processing_end_date",
        "Ошибка": "error_comment",
    })

    def fill_fields(self, filled_fields: Dict[str, str]) -> None:
        """Заполняет поля объекта на основе переданного словаря"""
        for key, value in filled_fields.items():
            # Проверяем, есть ли ключ в словаре меток
            if key in self.labels:
                attr_name = self.labels[key]
                setattr(self, attr_name, value)

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """Магический метод для итерации по полям, возвращая только заполненные значениями"""
        return (
            (label, getattr(self, attr_name))
            for label, attr_name in self.labels.items()
            if getattr(self, attr_name) is not None
        )

    def __repr__(self) -> str:
        """Переопределяем метод для более удобного отображения"""
        return (f"ReportRowData(employee_fullname={self.employee_fullname!r}, "
                f"registry={self.registry!r}, "
                f"document_name={self.document_name!r}, "
                f"branch={self.branch!r}, "
                f"personal_account={self.personal_account!r}, "
                f"inn={self.inn!r}, "
                f"contract_number={self.contract_number!r}, "
                f"contract_date={self.contract_date!r}, "
                f"document_date={self.document_date!r}, "
                f"document_id={self.document_id!r}, "
                f"status={self.status!r}, "
                f"processing_start_date={self.processing_start_date!r}, "
                f"processing_end_date={self.processing_end_date!r}, "
                f"error_comment={self.error_comment!r})")
