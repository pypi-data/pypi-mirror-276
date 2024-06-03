from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import inquirer
from inquirer.questions import Question

from breadslicer.components.base import BaseComponent


@dataclass
class ChoiceComponent(BaseComponent):
    default: Optional[str]
    choices: List[str] | List[Tuple[str, str]]
    ignore: Optional[Callable[[Dict[str, str | bool]], bool]]

    def component_question(self) -> Question:
        return inquirer.List(
            name=self.name,
            message=self.message,
            choices=self.choices,
            default=self.default,
            ignore=self.ignore,  # type: ignore
        )
