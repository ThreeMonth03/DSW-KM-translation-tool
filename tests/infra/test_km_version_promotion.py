"""Tests for automatic KM version promotion helpers."""

from __future__ import annotations

from pathlib import Path

import yaml

from dsw_translation_tool.km_version_promotion import (
    plan_version_promotions,
    update_supported_versions_in_config,
)
from dsw_translation_tool.translation_repository_config import load_translation_repository_config
from tests.infra.test_translation_repository_config import write_config


def test_plan_version_promotions_chains_from_latest_supported_version(workspace: Path) -> None:
    """Verify multiple new versions are planned as a sequential branch chain."""

    config_path = workspace / "translation-config.yml"
    write_config(config_path, supported_versions=["2.6.0", "2.7.0"])
    config = load_translation_repository_config(config_path)

    plans = plan_version_promotions(config, ["2.9.0", "2.8.0"])

    assert [(plan.version, plan.base_version, plan.base_branch, plan.branch) for plan in plans] == [
        ("2.8.0", "2.7.0", "translation/v2.7.0", "translation/v2.8.0"),
        ("2.9.0", "2.8.0", "translation/v2.8.0", "translation/v2.9.0"),
    ]


def test_update_supported_versions_in_config_adds_versions_once(workspace: Path) -> None:
    """Verify promotion updates supported KM versions in sorted order."""

    config_path = workspace / "translation-config.yml"
    write_config(config_path, supported_versions=["2.7.0"])

    merged = update_supported_versions_in_config(config_path, ["2.8.0", "2.7.0", "v2.9.0"])

    assert merged == ("2.7.0", "2.8.0", "2.9.0")
    payload = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    assert payload["knowledge_model"]["supported_versions"] == ["2.7.0", "2.8.0", "2.9.0"]


def test_update_supported_versions_preserves_localize_version_urls(workspace: Path) -> None:
    """Verify config updates do not drop Localize per-version URL mappings."""

    config_path = workspace / "translation-config.yml"
    write_config(config_path, supported_versions=["2.7.0"])
    payload = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    payload["localize"]["download_urls"] = {
        "2.7.0": "https://localize.ds-wizard.org/download/example/2.7.0/zh_Hant/",
    }
    config_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    update_supported_versions_in_config(config_path, ["2.8.0"])

    updated = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    assert updated["localize"]["download_urls"] == {
        "2.7.0": "https://localize.ds-wizard.org/download/example/2.7.0/zh_Hant/",
    }
