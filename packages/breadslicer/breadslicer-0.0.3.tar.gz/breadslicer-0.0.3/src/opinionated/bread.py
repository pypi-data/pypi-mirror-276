from pathlib import Path
from typing import Any, Dict, List, Tuple

from breadslicer.application.slice import BreadSlice
from breadslicer.components.base import BaseComponent
from breadslicer.components.choice import ChoiceComponent
from breadslicer.utility.command import PackageInstaller, poetry_install
from opinionated.cleanup import Finalize
from opinionated.dependencies import Dependencies
from opinionated.project_types import ProjectTypes
from opinionated.questions import Q


class OpinionatedBreadSlice(BreadSlice):
    includes_path: Path = Path(__file__).parent / "includes"
    templates_path: Path = Path(__file__).parent / "templates"
    excludes: List[str] = ["__pycache__/*"]

    """This is the opinionated breadslicer python project template"""

    @property
    def description(self) -> str:
        return (
            "This is the opinionated project template, "
            "choose project type, together with ci configurations."
        )

    @staticmethod
    def project_types() -> BaseComponent:
        p_types: List[Tuple[str, str]] = [
            ("Command-line application", ProjectTypes.app.value),
            ("Library", ProjectTypes.lib.value),
            ("Django application", ProjectTypes.django.value),
            ("Flask application", ProjectTypes.flask.value),
        ]
        return ChoiceComponent(
            name="project_type",
            message="[Project] What type of project is this?",
            default=None,
            choices=p_types,
            ignore=None,
        )

    def questions(self) -> List[BaseComponent]:
        """`questions` method of the `Bread` will implement the form
        to be entered by the user. It is split between project info, types, ci.
        """
        q: List[BaseComponent] = [
            *Q.project_info(),
            self.project_types(),
            Q.project_layout(),
            Q.git_hooks(),
            Q.ci_system(),
            Q.docker_base(),
        ]
        return q

    def pre_render(self, answers: Dict[Any, Any], directory: Path) -> None:
        pass

    def post_render(self, answers: Dict[Any, Any], directory: Path) -> None:
        installer = PackageInstaller(installer=poetry_install, directory=directory)
        deps = Dependencies(installer=installer, answers=answers)
        finalize = Finalize(answers=answers)

        # Install dependencies based on project type
        # Clean up afterwards
        match ProjectTypes[answers["project_type"]]:
            case ProjectTypes.app:
                deps.app()
                finalize.app()
            case ProjectTypes.lib:
                deps.lib()
                finalize.remove_main()
                finalize.lib()
            case ProjectTypes.django:
                deps.django()
                finalize.django()
            case ProjectTypes.flask:
                deps.flask()
                finalize.flask()
        finalize.docs()
        finalize.ci_install()
        finalize.pre_commit_hooks()
