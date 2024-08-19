import pandas as pd
from typing import NamedTuple
from logging import getLogger
from config.paths import MAPPING_BRANCHES


logger = getLogger(__name__)
HANDBOOK = pd.read_excel(open(MAPPING_BRANCHES, 'rb'), sheet_name='Филиалы')


class ReferenceData(NamedTuple):
    segment: str | None
    branch: str | None
    branch_id: str | None


class HandbookIndex:
    def __init__(self, account: str):
        self.account = account
        self.indexes = HANDBOOK.index[HANDBOOK['первые 3 цифры ЛС'] == int(account[:3])].tolist()

    def get_handbook_row_data(self) -> ReferenceData | None:
        try:
            return ReferenceData(
                segment='B2B',
                branch=str(HANDBOOK.loc[self.indexes[0], "Филиал"]).lower(),
                branch_id=str(HANDBOOK.loc[self.indexes[0], "BranchId (для ЕИП)"]).replace('.0', ''),
            )
        except Exception as e:
            logger.error(f"При попытке получить данные из справочника для ЛС{self.account} была получена ошибка {e}")
            return None
