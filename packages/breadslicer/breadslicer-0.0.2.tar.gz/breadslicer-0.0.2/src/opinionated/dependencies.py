from dataclasses import dataclass
from typing import Dict

from breadslicer.utility.command import PackageInstaller

DEVELOPMENT = ["isort", "black", "flake8", "mypy"]
DEV_GROUP = "dev"
DOCS = ["sphinx"]
TESTS = ["pytest", "pytest-cov"]
SECURITY = ["bandit"]
PRE_COMMIT = ["pre-commit"]


@dataclass
class Dependencies:
    installer: PackageInstaller
    answers: Dict[str, str]

    def dev_dependencies(self) -> None:
        self.installer.install_packages(
            DEVELOPMENT + TESTS + DOCS + SECURITY, group=DEV_GROUP
        )
        self.pre_commit_hooks()

    def django(self) -> None:
        self.dev_dependencies()
        self.installer.install_packages(
            ["django", "djangorestframework", "django-health-check"]
        )
        self.installer.install_packages(
            ["pytest-django", "django_stubs"], group=DEV_GROUP
        )

    def flask(self) -> None:
        self.dev_dependencies()
        self.installer.install_package("flask")

    def lib(self) -> None:
        self.dev_dependencies()
        self.installer.install_package("twine")

    def app(self) -> None:
        self.dev_dependencies()
        self.installer.install_package("twine")

    def pre_commit_hooks(self):
        self.installer.install_packages(PRE_COMMIT, group=DEV_GROUP)
