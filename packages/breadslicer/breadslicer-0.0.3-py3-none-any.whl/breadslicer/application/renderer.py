from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Set, Tuple, Type

from jinja2 import BaseLoader, Environment, FileSystemLoader, select_autoescape

from breadslicer.utility.abstractdataclass import AbstractDataclass


@dataclass
class Renderer(AbstractDataclass):
    includes_path: Path
    templates_path: Path
    excludes: List[str]

    @abstractmethod
    def loader(self) -> Type[BaseLoader]: ...

    def run(self, answers: Dict[Any, Any]) -> Iterator[Tuple[Path, Path, str]]:
        env = Environment(
            loader=FileSystemLoader(
                [self.templates_path.absolute(), self.includes_path.absolute()]
            ),
            autoescape=select_autoescape(),
        )
        files = self.find_files(self.templates_path)
        exclude_paths: Set[str] = set()
        for exclude in self.excludes:
            exclude_paths |= {
                str(x.absolute()) for x in self.templates_path.rglob(exclude)
            }

        for file in files:
            if str(file.absolute()) in exclude_paths:
                # If file is in the exclude path, skip it
                continue
            f = file.relative_to(self.templates_path)
            filename_template = env.from_string(str(f))
            template = env.get_template(str(f))
            yield file, Path(filename_template.render(answers)), template.render(
                answers
            )

    def find_files(self, path: Path) -> List[Path]:
        files: List[Path] = []
        for p in path.iterdir():
            if p.is_dir():
                files += self.find_files(p)
            elif p.is_file():
                files.append(p)
        return files


@dataclass
class FileSystemRenderer(Renderer):
    includes_path: Path
    templates_path: Path
    excludes: List[str]

    def loader(self) -> Type[BaseLoader]:
        return FileSystemLoader
