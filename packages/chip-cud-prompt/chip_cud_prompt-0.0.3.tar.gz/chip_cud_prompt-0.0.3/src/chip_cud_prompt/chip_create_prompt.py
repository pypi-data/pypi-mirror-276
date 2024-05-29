from .abstract_prompt_manager import AbstractPromptManager


class ChipCreatePrompt(AbstractPromptManager):
    @staticmethod
    def global_instruction() -> str:
        return """
        Hello world
        """

    @property
    def message_instruction(self) -> str:
        return self.global_instruction()

    @property
    def image_instruction(self) -> str:
        return self.global_instruction()

    @property
    def file_instruction(self) -> str:
        return self.global_instruction()

    @property
    def target(self) -> str:
        return """
        hello world target
        """
