class TypeErrorTable(Exception):
    """Ошибка Объекта таблицы/Таблица не соответствует шаблона"""
    pass


class TypeErrorDocx(Exception):
    """Ошибка неподходящего типа объекта"""
    pass


class UnknownValidatingClasses(Exception):
    """Ошибка неизвестных объектов-валидаторов для проверок путей к файлам/папкам на сетевых ресурсах"""
    pass


class AccessModeError(Exception):
    """Ошибка выбора режима доступа"""
    pass


class FileTemplateError(Exception):
    """Файл не соответствует шаблону"""
    pass


class RowValidateError(Exception):
    """Ошибка валидации строки таблицы"""
    pass
