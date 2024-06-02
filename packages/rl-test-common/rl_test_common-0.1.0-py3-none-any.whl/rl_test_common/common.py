from .singleton_meta import SingletonMeta


class Common(metaclass=SingletonMeta):
    __user_files_root: str = 'user_files'

    @property
    def user_files_root(self) -> str:
        return self.__user_files_root

    def get_type(self, obj: object) -> str:
        return type(obj).__name__
