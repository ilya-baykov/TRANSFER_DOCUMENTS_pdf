from typing import List

import pandas as pd
from logging import getLogger

logger = getLogger(__name__)


class TableDataFrameCreator:
    def __init__(self, data: List[List[str]]):
        self.__df = pd.DataFrame(data)
        self.__df_preparation()

    def __df_preparation(self):
        """Приводит табличный датафрейм в нужный вид"""
        self.__df.columns = self.__df.iloc[0].str.replace('\n', '')  # Удаление переносов строк в названиях колонок
        self.__df = self.__df.drop(index=0).reset_index(drop=True)  # Удаляем первую строку (заголовок)

    def get_df(self) -> pd.DataFrame:
        """Возвращает подготовленный табличный датафрейм"""
        return self.__df
