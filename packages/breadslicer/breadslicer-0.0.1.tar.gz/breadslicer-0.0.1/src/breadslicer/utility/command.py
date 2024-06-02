import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional


def cmd(
    commands: List[str],
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
) -> None:
    subprocess.run(
        commands, capture_output=False, check=True, shell=False, cwd=cwd, env=env
    )


def capture_cmd(commands: List[str], cwd: Optional[Path] = None) -> str:
    rc: subprocess.CompletedProcess[bytes] = subprocess.run(
        commands, capture_output=True, check=True, cwd=cwd
    )
    if rc.returncode == 0:
        return rc.stdout.decode("utf-8")
    else:
        raise RuntimeError(
            f"ERROR running command {' '.join(commands)}:\n {rc.stderr!r}"
        )


def poetry_run(commands: List[str], cwd: Optional[Path] = None) -> None:
    cmd(["poetry", "run"] + commands, cwd)


def poetry_install(
    package: str, group: Optional[str] = None, cwd: Optional[Path] = None
) -> None:
    # TODO: Make sure that we can get poetry's location
    poetry_bin = capture_cmd(["which", "poetry"]).replace("\n", "")
    if group:
        cmd(
            [
                poetry_bin,
                "add",
                package,
                f"--group={group}",
            ],
            cwd=cwd,
            env={},
        )
    else:
        cmd([poetry_bin, "add", package], cwd=cwd, env={})


@dataclass
class PackageInstaller:
    installer: Callable[[str, Optional[str], Optional[Path]], None]
    directory: Path

    def install_package(self, package: str, group: Optional[str] = None) -> None:
        self.installer(package, group, self.directory)

    def install_packages(
        self, packages: List[str], group: Optional[str] = None
    ) -> None:
        for package in packages:
            self.install_package(package, group=group)
