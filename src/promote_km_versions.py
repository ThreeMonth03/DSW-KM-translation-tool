#!/usr/bin/env python3
"""Promote newly discovered KM versions into translation branches."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dsw_translation_tool.km_version_promotion import (
    KmVersionPromotionError,
    promote_new_km_versions,
)


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description="Create version branches for newly discovered KM package versions.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Translation repository checkout root.",
    )
    parser.add_argument(
        "--tooling-repo",
        default=".",
        help="Tooling repository checkout root.",
    )
    parser.add_argument(
        "--config",
        default="translation-config.yml",
        help="Path to translation-config.yml relative to repo root.",
    )
    parser.add_argument(
        "--registry-token-env",
        default="DSW_REGISTRY_TOKEN",
        help="Environment variable containing the DSW Registry token.",
    )
    parser.add_argument(
        "--skip-without-token",
        action="store_true",
        help="Exit successfully when new versions exist but the token is missing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan promotions without changing branches or files.",
    )
    parser.add_argument(
        "--max-new-versions",
        type=int,
        default=None,
        help="Optional cap on the number of new versions promoted in one run.",
    )
    return parser


def main() -> None:
    """Run KM version promotion."""

    args = build_argument_parser().parse_args()
    token = os.environ.get(args.registry_token_env, "")
    try:
        result = promote_new_km_versions(
            repo_root=Path(args.repo_root),
            tooling_repo=Path(args.tooling_repo),
            config_path=Path(args.config),
            registry_token=token,
            skip_without_token=args.skip_without_token,
            dry_run=args.dry_run,
            max_new_versions=args.max_new_versions,
        )
    except KmVersionPromotionError as error:
        raise SystemExit(f"Unable to promote KM versions: {error}") from error

    if not result.plans:
        print("No new KM versions discovered.")
        return
    print("KM version promotion plan:")
    for plan in result.plans:
        print(
            f"  {plan.version}: {plan.base_branch} -> {plan.branch} "
            f"(base version {plan.base_version})"
        )
    if result.skipped_reason:
        print(f"Skipped promotion: {result.skipped_reason}")
        return
    if result.dry_run:
        print("Dry run only; no branches were changed.")
        return
    print("Promoted versions: " + ", ".join(result.promoted_versions))


if __name__ == "__main__":
    main()
