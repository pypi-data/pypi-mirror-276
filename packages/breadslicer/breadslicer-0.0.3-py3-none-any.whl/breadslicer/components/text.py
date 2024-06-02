from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

import inquirer
from inquirer.questions import Question

from breadslicer.components.base import BaseComponent
from breadslicer.utility.git import get_author_from_git, get_email_from_git


@dataclass
class TextComponent(BaseComponent):
    default: Optional[str | Callable[[Dict[str, str]], str]]

    def component_question(self) -> Question:
        return inquirer.Text(
            name=self.name,
            message=self.message,
            default=self.default,
        )


@dataclass
class AuthorComponent(BaseComponent):
    default: Optional[str | Callable[[Dict[str, str]], str]] = field(
        default_factory=get_author_from_git
    )

    def component_question(self) -> Question:
        return inquirer.Text(
            name=self.name,
            message=self.message,
            default=self.default,
        )


@dataclass
class EmailComponent(BaseComponent):
    default: Optional[str | Callable[[Dict[str, str]], str]] = field(
        default_factory=get_email_from_git
    )

    def component_question(self) -> Question:
        return inquirer.Text(
            name=self.name,
            message=self.message,
            default=self.default,
        )
