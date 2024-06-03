from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from breadslicer.components.base import BaseComponent


class BreadSlice(ABC):

    includes_path: Path = Path("src/opinionated/includes")
    templates_path: Path = Path("src/opinionated/templates")

    excludes = ["__pycache__/*"]

    @property
    @abstractmethod
    def description(self) -> str: ...

    def preamble(self) -> None:
        """The preamble method will be called before everything else.

        This is generally used to check for run time dependencies

        Overload it as you see fit.

        """
        return None

    @abstractmethod
    def questions(self) -> List[BaseComponent]:
        """Questions method needs to be implemented and needs to return Components.

        This will be called as the first step before rendering of templates.
        This needs to be implemented if no `breadslicer.yaml` file is used.
        """
        ...

    def pre_render(self, answers: Dict[Any, Any], directory: Path) -> None:
        """The pre-render method will be called after questions
        and before pre_render.

        Overload it as you see fit.

        Keywords arguments:
        answers -- Dictionary containing the response from the user
        directory -- Path to output directory
        """
        return None

    def post_render(self, answers: Dict[Any, Any], directory: Path) -> None:
        """The post-render method will be called after questions and pre_render.

        It is generally used to remove unwanted files and install packages based
        on the answers given earlier.

        Overload it as you see fit

        Keywords arguments:
        answers -- Dictionary containing the response from the user
        directory -- Path to output directory
        """
        return None
