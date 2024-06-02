from dataclasses import dataclass
from typing import List, Optional

import inquirer
from inquirer.questions import Question

from breadslicer.components.base import BaseComponent


@dataclass
class MultipleChoiceComponent(BaseComponent):
    default: Optional[List[str]]
    choices: List[str]

    def component_question(self) -> Question:
        return inquirer.Checkbox(
            name=self.name,
            message=self.message,
            choices=self.choices,
            default=self.default,
        )
