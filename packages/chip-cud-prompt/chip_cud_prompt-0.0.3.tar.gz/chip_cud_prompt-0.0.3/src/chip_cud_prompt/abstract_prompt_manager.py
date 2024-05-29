from abc import ABC, abstractmethod


class AbstractPromptManager(ABC):
    @abstractmethod
    @property
    def message_instruction(self) -> str:
        pass

    @abstractmethod
    @property
    def image_instruction(self) -> str:
        pass

    @abstractmethod
    @property
    def file_instruction(self) -> str:
        pass

    @abstractmethod
    @property
    def target(self) -> str:
        pass
