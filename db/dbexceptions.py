# encoding=utf-8


class WarningException(StandardError):
    """警告异常基类"""

    def __init__(self, *args, **kwargs):
        pass


class ErrorException(BaseException):
    """错误异常基类"""

    def __init__(self, *args, **kwargs):
        pass


class InterfaceErrorException(ErrorException):
    """数据库接口错误"""

    def __init__(self, *args, **kwargs):
        pass


class DatabaseErrorException(ErrorException):
    """数据库错误"""

    def __init__(self, *args, **kwargs):
        pass


class DataErrorException(DatabaseErrorException):
    """处理数据时出错"""

    def __init__(self, *args, **kwargs):
        pass


class OperationalErrorException(DatabaseErrorException):
    """数据库执行命令时出错"""

    def __init__(self, *args, **kwargs):
        pass


class IntegrityErrorException(DatabaseErrorException):
    """数据完整性错误"""

    def __init__(self, *args, **kwargs):
        pass


class InternalErrorException(DatabaseErrorException):
    """数据库内部出错"""

    def __init__(self, *args, **kwargs):
        pass


class ProgrammingErrorException(DatabaseErrorException):
    """SQL 执行失败"""

    def __init__(self, *args, **kwargs):
        pass


class NotSupportedErrorException(DatabaseErrorException):
    """试图执行数据库不支持的特性"""

    def __init__(self, *args, **kwargs):
        pass
