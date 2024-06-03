from dataclasses import dataclass
from typing import Optional

import inquirer  # type: ignore
from inquirer.questions import Question  # type: ignore

from breadslicer.components.base import BaseComponent


@dataclass
class ConfirmComponent(BaseComponent):

    default: Optional[bool]

    def component_question(self) -> Question:
        assert isinstance(self.default, bool)
        return inquirer.Confirm(
            name=self.name, message=self.message, default=self.default
        )
