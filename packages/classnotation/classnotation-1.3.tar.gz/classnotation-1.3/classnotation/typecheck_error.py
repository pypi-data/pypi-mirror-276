from typing import Tuple

class TypeCheckError(Exception):
    message: str
    stack: Tuple[str, ...]
    def __init__(self, message: str, stack: Tuple[str, ...]):
        self.message = message
        self.stack = stack
        pass

    def __str__(self) -> str:
        return "{stack}: {message}".format(
            stack=".".join(self.stack),
            message=self.message,
        )
