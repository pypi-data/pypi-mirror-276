import argparse
from pathlib import Path
from typing import Any, Dict, Optional

import inquirer
import inquirer.themes

from breadslicer.application.renderer import FileSystemRenderer
from breadslicer.application.slice import BreadSlice
from breadslicer.utility import fs
from opinionated.bread import OpinionatedBreadSlice


class Application:
    source: str
    bread: BreadSlice
    output: Optional[Path]

    def __init__(self, url: str, args: argparse.Namespace) -> None:
        self.source = url
        self.bread = self._resolve_slice()
        if args.output:
            self.output = args.output
        else:
            self.output = None

    def run(self) -> None:
        self.bread.preamble()

        self.print(self.bread.description)

        answers = self.ask()

        self.bread.pre_render(answers=answers, directory=self.directory(answers))

        self.render(answers=answers)

        # TODO: This should be replaced by an objects that operates specifically on
        # different base paths.
        fs.cwd(self.directory(answers=answers))

        self.bread.post_render(answers=answers, directory=self.directory(answers))

    def directory(self, answers: Dict[Any, Any]) -> Path:
        if self.output:
            return self.output / Path(answers["project_slug"])
        else:
            return Path(answers["project_slug"])

    def print(self, *args: str) -> None:
        print(*args)

    def _resolve_slice(self) -> BreadSlice:
        """Resolve what type of bread slice is source.

        Possibilities are the default opinionated templates, a local directory
        or a external url to a git repository.
        """
        match self.source:
            case "opinionated":
                # Default case, use the builtin template
                return self.resolve_opinionated()
            case _:
                raise ValueError(f'Could not resolve project from "{self.source}"')

    def resolve_opinionated(self) -> BreadSlice:
        return OpinionatedBreadSlice()

    def render(self, answers: Dict[Any, Any]) -> None:
        render = FileSystemRenderer(
            templates_path=self.bread.templates_path,
            includes_path=self.bread.includes_path,
            excludes=self.bread.excludes,
        )

        directory = self.directory(answers)

        directory.mkdir()

        for origin, path, content in render.run(answers=answers):

            file = directory / path
            # Create directory and write content
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(content)

            # Set file permissions
            permissions = origin.stat().st_mode
            file.chmod(permissions)

    def ask(self) -> Dict[str, str]:
        questions = self.bread.questions()
        return inquirer.prompt(  # type: ignore
            questions=[q.component_question() for q in questions],
            theme=inquirer.themes.GreenPassion(),
            raise_keyboard_interrupt=True,
        )
