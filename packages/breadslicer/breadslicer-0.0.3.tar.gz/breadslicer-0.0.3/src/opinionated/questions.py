import sys
from typing import Dict, List, Tuple

from breadslicer.components.base import BaseComponent
from breadslicer.components.choice import ChoiceComponent
from breadslicer.components.confirm import ConfirmComponent
from breadslicer.components.editor import EditorComponent
from breadslicer.components.text import AuthorComponent, EmailComponent, TextComponent


class Q:
    @staticmethod
    def is_service(answers: Dict[str, str | bool]) -> bool:
        """Utility function to determine if the project type
        is a service.
        """
        none_service_types = {"app", "lib"}
        return (
            answers["project_type"] not in none_service_types
            if "project_type" in answers
            else False
        )

    @staticmethod
    def is_not_service(answers: Dict[str, str | bool]) -> bool:
        """Utility function to determine if the project type
        is a not service.
        """
        none_service_types = {"app", "lib"}
        return (
            answers["project_type"] in none_service_types
            if "project_type" in answers
            else False
        )

    @classmethod
    def project_layout(cls) -> BaseComponent:
        layouts: List[Tuple[str, str]] = [
            ("Flat layout", "flat"),
            ("Source layout", "src"),
        ]
        return ChoiceComponent(
            name="project_layout",
            message="[Project] Choose the project layout",
            default=None,
            choices=layouts,
            ignore=cls.is_service,
        )

    def build_system(self) -> BaseComponent:
        systems: List[Tuple[str, str]] = [
            ("Poetry", "poetry"),
            ("Setuptools", "src"),
        ]
        return ChoiceComponent(
            name="build_system",
            message="[Build] Select build system",
            default=None,
            choices=systems,
            ignore=self.is_not_service,
        )

    @staticmethod
    def git_hooks() -> BaseComponent:
        return ConfirmComponent(
            name="use_commit_hooks",
            message="[GIT] Do you want to use git commit hooks "
            "to run verify before commits?",
            default=True,
        )

    @staticmethod
    def ci_system() -> BaseComponent:
        systems: List[Tuple[str, str]] = [
            ("Gitlab", "gitlab"),
            ("No CI system", "none"),
        ]
        return ChoiceComponent(
            name="ci_system",
            message="[CI] What CI system should be used?",
            default="gitlab",
            choices=systems,
            ignore=None,
        )

    @staticmethod
    def docker_base() -> BaseComponent:
        docker_images: List[Tuple[str, str]] = [
            ("alpine", "alpine"),
            ("debian", "debian"),
            ("debian-slim", "slim"),
        ]
        return ChoiceComponent(
            name="docker_base",
            message="[Docker] Select base python docker image from dockerhub",
            default="debian",
            choices=docker_images,
            ignore=None,
        )

    @staticmethod
    def project_info() -> List[BaseComponent]:
        ver = sys.version_info
        python_version = f"{ver.major}.{ver.minor}.{ver.micro}"

        project_name = TextComponent(
            name="project_name",
            message="[Project] Project name",
            default="",
        )
        project_slug = TextComponent(
            name="project_slug",
            message="[Project] Project slug",
            default=lambda answers: answers["project_name"]
            .lower()
            .replace(" ", "_")
            .replace("-", "_"),
        )
        project_author_name = AuthorComponent(
            name="project_author_name",
            message="[Project] Type in name of the author",
        )
        project_author_email = EmailComponent(
            name="project_author_email", message="[Project] Type in email of author"
        )
        project_short_description = EditorComponent(
            name="project_short_description",
            message="[Project] Type in short project description",
        )
        project_python_version = TextComponent(
            "PYTHON_VERSION",
            "Type in the python version",
            default=python_version,
        )

        return [
            project_name,
            project_slug,
            project_author_name,
            project_author_email,
            project_short_description,
            project_python_version,
        ]
