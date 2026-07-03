"""Tests for packaged command-line entry point wiring."""

from __future__ import annotations

import importlib
import tomllib
from collections.abc import Mapping
from pathlib import Path


def load_project_scripts(repo_root: Path) -> Mapping[str, str]:
    """Return console script declarations from `pyproject.toml`."""

    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    return pyproject["project"]["scripts"]


def test_console_scripts_are_packaged_cli_modules(repo_root: Path) -> None:
    """Verify every public command resolves to a packaged CLI `main` function."""

    scripts = load_project_scripts(repo_root)

    assert scripts
    for command_name, target in scripts.items():
        assert command_name.startswith("dsw-km-")
        module_name, function_name = target.split(":", maxsplit=1)
        assert module_name.startswith("dsw_km_translation_tool.cli.")
        assert function_name == "main"

        module = importlib.import_module(module_name)
        assert callable(getattr(module, function_name))
