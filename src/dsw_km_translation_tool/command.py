"""Shared subprocess and Git helpers for automation workflows."""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Protocol

GITHUB_BOT_NAME = "github-actions[bot]"
GITHUB_BOT_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"

ErrorFactory = Callable[[str], Exception]


class CommandRunner(Protocol):
    """Protocol for injectable subprocess execution."""

    def __call__(
        self,
        args: Sequence[str],
        *,
        cwd: Path,
        env: Mapping[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run one command and return the completed-process result."""


def default_command_runner(
    args: Sequence[str],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run one subprocess command with captured text output."""

    command_env = os.environ.copy()
    if env:
        command_env.update(env)
    return subprocess.run(
        list(args),
        cwd=str(cwd),
        env=command_env,
        capture_output=True,
        text=True,
        check=False,
    )


def tooling_virtualenv_command_path(tooling_repo_dir: Path, command_name: str) -> Path:
    """Return one console-script path from a tooling repository virtualenv."""

    return tooling_repo_dir / ".venv" / "bin" / command_name


def tooling_virtualenv_python_path(tooling_repo_dir: Path) -> Path:
    """Return the Python executable path from a tooling repository virtualenv."""

    return tooling_virtualenv_command_path(tooling_repo_dir, "python")


def make_checked_runner(
    error_factory: ErrorFactory,
    *,
    include_command: bool,
) -> Callable[..., subprocess.CompletedProcess[str]]:
    """Return a module-specific checked runner with consistent failure output."""

    def checked_runner(
        runner: CommandRunner,
        args: Sequence[str],
        *,
        cwd: Path,
        description: str,
        env: Mapping[str, str] | None = None,
        echo_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        return run_checked(
            runner,
            args,
            cwd=cwd,
            description=description,
            error_factory=error_factory,
            env=env,
            echo_output=echo_output,
            include_command=include_command,
        )

    return checked_runner


def run_checked(
    runner: CommandRunner,
    args: Sequence[str],
    *,
    cwd: Path,
    description: str,
    error_factory: ErrorFactory,
    env: Mapping[str, str] | None = None,
    echo_output: bool = False,
    include_command: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run one command and raise a caller-specific error on failure."""

    result = runner(args, cwd=cwd, env=env)
    if echo_output:
        print_process_output(result)
    if result.returncode == 0:
        return result

    output = (result.stderr or result.stdout or "").strip()
    command = " ".join(str(part) for part in args)
    if include_command:
        if output:
            raise error_factory(f"Failed to {description}: {command}\n{output}")
        raise error_factory(f"Failed to {description}: {command}")
    raise error_factory(f"Failed to {description}: {output}")


def configure_github_actions_git_identity(
    *,
    repo_root: Path,
    runner: CommandRunner,
    error_factory: ErrorFactory,
    include_command: bool,
) -> None:
    """Configure the standard GitHub Actions bot identity in one repository."""

    checked = make_checked_runner(error_factory, include_command=include_command)
    checked(
        runner,
        ["git", "config", "user.name", GITHUB_BOT_NAME],
        cwd=repo_root,
        description="configure git bot name",
    )
    checked(
        runner,
        ["git", "config", "user.email", GITHUB_BOT_EMAIL],
        cwd=repo_root,
        description="configure git bot email",
    )


def print_process_output(result: subprocess.CompletedProcess[str]) -> None:
    """Relay captured subprocess output to the current stdout stream."""

    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")
