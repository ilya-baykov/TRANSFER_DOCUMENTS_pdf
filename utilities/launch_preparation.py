import os
from abc import ABC, abstractmethod
from logging import getLogger

from config.paths import PATH_FILES, MAPPING_BRANCHES, PATH_REPORTS, PATH_TEMPLATE_REPORTS, PATH_DELETE
from exeptions import UnknownValidatingClasses, AccessModeError

logger = getLogger(__name__)


class AvailabilityChecker(ABC):
    @abstractmethod
    def availability_check(self, path: str) -> bool:
        """Метод для проверки наличия файла/папки на сетевом ресурсе"""
        pass


class AvailabilityCheckerWithOutCreation(AvailabilityChecker):
    """Класс для проверки наличия файла/папки на сетевом ресурсе без дальнейшего создания"""

    def availability_check(self, path: str) -> bool:
        try:
            if os.path.exists(path):
                logger.info(f"По пути: {path} был найден файл")
                return True

            logger.error(f"Не удалось найти файл/папку с таким путём : {path} ")
            return False

        except Exception as e:
            logger.error(f"При попытке проверить наличие файла/папки по пути {path} произошла ошибка {e}")
            return False


class AvailabilityCheckerWithCreation(AvailabilityChecker):
    """Класс для проверки наличия файла/папки на сетевом ресурсе
    с дальнейшим созданием этого файла/папки при его/её отсутствии"""

    def availability_check(self, path: str) -> bool:
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"При попытке проверить наличие (или создания) файла/пути   : {path}  произошла ошибка ")
            return False


class AccessChecker:
    def __init__(self, mode: os.R_OK):
        """
        :param mode: Устанавливает режим проверки доступа (на чтение-os.R_OK, на запись-os.W_Ok)
        """
        if mode in (os.R_OK, os.W_OK):
            self.mode = mode
        else:
            raise AccessModeError

    def check_access(self, path: str) -> bool:
        """Метод для проверки доступа к ресурсу с определенным режимом (на чтение/на запись)"""
        try:
            if os.access(path, self.mode):
                logger.info(f"Для Ресурса: {path} есть доступ {self.mode}")
                return True
            logger.error(f"Для Ресурса: {path} нет доступа {self.mode}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при попытке проверить доступ {self.mode} к {path}")
            return False


class PathResourceChecker:
    """Класс для проверки доступа к сетевому ресурсу"""

    def __init__(self, path_resource: str, availability_checker, access_checker: AccessChecker):
        """

        :param path_resource: Путь к ресурсу для проверки
        :param availability_checker:  Объект AvailabilityChecker
        :param access_checker: Объект AccessChecker
        """
        self.path_resource = path_resource
        if isinstance(availability_checker, AvailabilityChecker) and isinstance(access_checker, AccessChecker):
            self.availability_checker = availability_checker
            self.access_checker = access_checker
        else:
            raise UnknownValidatingClasses

    def get_verdict(self) -> bool:
        """Возвращает результат проверок"""
        return self.__availability_check() and self.__check_access()

    def __check_access(self) -> bool:
        """Метод для проверки доступа на чтение к ресурсу"""
        return self.access_checker.check_access(self.path_resource)

    def __availability_check(self) -> bool:
        """Проверка наличия файла/папки на сетевом ресурсе"""
        return self.availability_checker.availability_check(self.path_resource)


class LaunchPreparer:
    _read_mode_access_checker = AccessChecker(mode=os.R_OK)  # Проверка доступа на чтение
    _writ_mode_access_checker = AccessChecker(mode=os.W_OK)  # Проверка доступа на запись
    _availability_checker_with_out_creation = AvailabilityCheckerWithOutCreation()  # Проверить наличие файла/папки
    _availability_checker_with_creation = AvailabilityCheckerWithCreation()  # Проверить наличие/создать файл/папку

    @classmethod
    def is_ready_launch(cls):
        # Файлы на обработку
        _processing_files_paths = PathResourceChecker(path_resource=PATH_FILES,
                                                      access_checker=cls._read_mode_access_checker,
                                                      availability_checker=cls._availability_checker_with_out_creation)
        # Шаблон отчёта Акт об утере ДД
        _template_reports_path = PathResourceChecker(path_resource=PATH_TEMPLATE_REPORTS,
                                                     access_checker=cls._read_mode_access_checker,
                                                     availability_checker=cls._availability_checker_with_out_creation)
        # Справочник филиалов
        _handbook_file_path = PathResourceChecker(path_resource=MAPPING_BRANCHES,
                                                  access_checker=cls._read_mode_access_checker,
                                                  availability_checker=cls._availability_checker_with_out_creation)

        # Файлы отчётов
        _reports_files_paths = PathResourceChecker(path_resource=PATH_REPORTS,
                                                   access_checker=cls._writ_mode_access_checker,
                                                   availability_checker=cls._availability_checker_with_creation)
        # Файлы в корзине
        _delete_files_paths = PathResourceChecker(path_resource=PATH_DELETE,
                                                  access_checker=cls._writ_mode_access_checker,
                                                  availability_checker=cls._availability_checker_with_creation)

        _all_checks = (_processing_files_paths, _template_reports_path, _handbook_file_path,
                       _reports_files_paths, _delete_files_paths)

        return all(verdict.get_verdict() for verdict in _all_checks)
