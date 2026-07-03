"""Helpers for pulling Localize/Weblate PO snapshots into translation branches."""

from __future__ import annotations

import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .translation_repository_config import (
    load_translation_repository_config,
    version_paths,
)

Downloader = Callable[[str], bytes]


@dataclass(frozen=True)
class LocalizePullResult:
    """Summary of one Localize PO pull."""

    version: str
    url: str
    base_po_path: Path | None
    latest_po_path: Path
    changed: bool
    initialized: bool
    bytes_downloaded: int


def pull_localize_po(
    *,
    config_path: Path,
    repo_root: Path,
    km_version: str | None = None,
    downloader: Downloader | None = None,
    base_snapshot_path: Path | None = None,
) -> LocalizePullResult:
    """Download and store the latest Localize PO snapshot.

    When ``base_snapshot_path`` is provided, the previous checked-in
    ``latest.po`` snapshot is copied there before the new latest snapshot is
    written. First pulls use the downloaded PO as that base. This lets sync
    jobs run a three-way merge without tracking a separate ``base.po`` file in
    the translation repository.

    Args:
        config_path: Path to ``translation-config.yml``.
        repo_root: Translation repository checkout root.
        km_version: KM version to pull. Defaults to the latest configured
            supported version.
        downloader: Optional injectable downloader used by tests.
        base_snapshot_path: Optional temporary path where the previous latest
            snapshot should be written for downstream merge reporting.

    Returns:
        Pull summary.
    """

    repository_config = load_translation_repository_config(config_path)
    version = km_version or repository_config.knowledge_model.supported_versions[-1]
    paths = version_paths(repository_config, version)
    latest_po_path = repo_root / paths.localize_latest_po_path
    url = repository_config.localize.download_url
    download = downloader or _download_url
    downloaded = download(url)

    latest_exists = latest_po_path.exists()
    previous_latest = latest_po_path.read_bytes() if latest_exists else None
    if base_snapshot_path is not None:
        base_snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        base_snapshot_path.write_bytes(
            previous_latest if previous_latest is not None else downloaded
        )

    if previous_latest == downloaded:
        return LocalizePullResult(
            version=version,
            url=url,
            base_po_path=base_snapshot_path,
            latest_po_path=latest_po_path,
            changed=False,
            initialized=False,
            bytes_downloaded=len(downloaded),
        )

    latest_po_path.parent.mkdir(parents=True, exist_ok=True)
    latest_po_path.write_bytes(downloaded)

    return LocalizePullResult(
        version=version,
        url=url,
        base_po_path=base_snapshot_path,
        latest_po_path=latest_po_path,
        changed=True,
        initialized=previous_latest is None,
        bytes_downloaded=len(downloaded),
    )


def _download_url(url: str) -> bytes:
    """Download one URL using the Python standard library."""

    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()
