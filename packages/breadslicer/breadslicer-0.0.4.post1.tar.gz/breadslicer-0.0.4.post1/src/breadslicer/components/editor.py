from dataclasses import dataclass
from typing import Optional

import inquirer  # type: ignore
from inquirer.questions import Question  # type: ignore

from breadslicer.components.base import BaseComponent


@dataclass
class EditorComponent(BaseComponent):
    default: Optional[str] = None

    def component_question(self) -> Question:
        return inquirer.Editor(
            name=self.name,
            message=self.message,
            default=self.default,
        )
