from abc import ABC, abstractmethod


class UpdateImage(ABC):
    s_update_func_list = []

    def __init__(self, update_iamge: 'UpdateImage', name: str) -> None:
        UpdateImage.s_update_func_list.append(update_iamge)
        self.name = name

    @staticmethod
    def get_update_func(name: str) -> 'UpdateImage':
        for func in UpdateImage.s_update_func_list:
            if func.get_name() == name:
                return func
        return None

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def update(self, path:str) -> bool:
        pass

    def __str__(self) -> str:
        return self.name
