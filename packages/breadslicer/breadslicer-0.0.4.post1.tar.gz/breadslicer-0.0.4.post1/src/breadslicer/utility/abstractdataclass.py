from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args: Any, **kwargs: Any):
        if cls == AbstractDataclass or cls.__bases__[0] == AbstractDataclass:
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)
