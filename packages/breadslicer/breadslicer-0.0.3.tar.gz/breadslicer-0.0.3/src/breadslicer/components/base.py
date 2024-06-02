from abc import abstractmethod
from dataclasses import dataclass

from inquirer.questions import Question  # type: ignore

from breadslicer.utility.abstractdataclass import AbstractDataclass


@dataclass
class BaseComponent(AbstractDataclass):
    name: str
    message: str

    @abstractmethod
    def component_question(self) -> Question: ...
