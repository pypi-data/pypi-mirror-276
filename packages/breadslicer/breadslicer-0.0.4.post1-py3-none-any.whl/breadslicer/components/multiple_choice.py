from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import inquirer
from inquirer.questions import Question

from breadslicer.components.base import BaseComponent


@dataclass
class MultipleChoiceComponent(BaseComponent):
    default: Optional[List[str]]
    choices: List[str]
    ignore: Optional[Callable[[Dict[str, str | bool]], bool]] = None

    def component_question(self) -> Question:
        return inquirer.Checkbox(
            name=self.name,
            message=self.message,
            choices=self.choices,
            default=self.default,
            ignore=self.ignore,  # type: ignore
        )
